import datetime

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
        content = tools.load_full_content(driver=self.driver, url=response.url)
        res = response.replace(body=content)
        self.driver.close()

        tournaments = res.css('ms-event-group')

        for t in tournaments:
            t_name = tools.extract_name(t.css('div div span::text').get())
            for e in t.css('ms-event'):
                loader = ItemLoader(item=EventItem(), selector=e)
                players = e.css('div.participant::text').getall()
                start_date = e.css('ms-prematch-timer::text').get()
                odds = e.css('ms-font-resizer::text').getall()
                lastUpdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                event_name, player1, player2 = tools.players_parser(players)

                loader.add_value('tournament', t_name)
                loader.add_value('eventName', event_name)
                loader.add_value('player1', player1)
                loader.add_value('player2', player2)
                loader.add_value('player1_odds', odds)
                loader.add_value('player2_odds', odds)
                loader.add_value('eventDate', start_date)
                loader.add_value('lastUpdate', lastUpdate)

                # Do not save events already started/live
                if start_date:
                    yield loader.load_item()



