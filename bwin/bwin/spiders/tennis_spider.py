from webdriver_manager.chrome import ChromeDriverManager
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy import Spider
import datetime

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
        self.driver.close()

        tournaments = res.css('ms-event-group')

        for t in tournaments:
            t_name = tools.t_name_parser(t.css('div div span::text').get())
            for e in t.css('ms-event'):
                loader = ItemLoader(item=EventItem(), selector=e)

                start_date = e.css('ms-prematch-timer::text').get()
                start_soon = e.css('ms-prematch-timer b::text').get()
                players = e.css('div.participant::text').getall()
                odds = e.css('ms-font-resizer::text').getall()

                e_name, player1, player2 = tools.players_parser(players)
                last_update = tools.update_parser(tools.get_now_utc())
                full_date = tools.event_date_parser(start_date, start_soon)

                loader.add_value('lastUpdate', last_update)
                loader.add_value('eventDate', full_date)
                loader.add_value('player1_odds', odds)
                loader.add_value('player2_odds', odds)
                loader.add_value('tournament', t_name)
                loader.add_value('eventName', e_name)
                loader.add_value('player1', player1)
                loader.add_value('player2', player2)

                # Save only events not started/live yet
                if start_date:
                    yield loader.load_item()

