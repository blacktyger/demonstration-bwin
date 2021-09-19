from webdriver_manager.chrome import ChromeDriverManager
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy import Spider

from ..items import EventItem
from .. import tools
from .. import paths


class TennisSpider(Spider):
    name = "tennis"
    start_urls = [paths.TENNIS_URL]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize selenium web-driver through https://pypi.org/project/webdriver-manager/
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parse(self, response, **kwargs):
        """Main scrapy logic is here"""
        content = tools.load_full_content(driver=self.driver, url=response.url)
        res = response.replace(body=content)

        tournaments = res.css('ms-event-group')

        for t in tournaments:
            for e in t.css('ms-event'):  # for e in events
                loader = ItemLoader(item=EventItem(), selector=e)

                start_soon = e.css('ms-prematch-timer b::text').get()
                start_date = e.css('ms-prematch-timer::text').get()
                players = e.css('div.participant::text').getall()
                odds = e.css('ms-option-group')
                p1_odds = odds.xpath(paths.P1_ODDS).get()
                p2_odds = odds.xpath(paths.P2_ODDS).get()

                last_update = tools.convert_dt_to_str(tools.get_now_utc())
                ready_odds = [tools.odds_parser(x) for x in [p1_odds, p2_odds]]
                full_date = tools.date_parser(start_date, start_soon)
                p1, p2 = tools.players_parser(players)[1:3]
                e_name = tools.players_parser(players)[0]
                t_name = tools.t_name_parser(t.css('div div span::text').get())

                loader.add_value('tournament', t_name)
                loader.add_value('eventName', e_name)
                loader.add_value('player1', p1)
                loader.add_value('player2', p2)
                loader.add_value('player1_odds', ready_odds[0])
                loader.add_value('player2_odds', ready_odds[1])
                loader.add_value('eventDate', full_date)
                loader.add_value('lastUpdate', last_update)

                # Save only events not started/live and where odds are available
                if start_date and ready_odds and players and e_name and t_name:
                    yield loader.load_item()

        self.driver.close()
