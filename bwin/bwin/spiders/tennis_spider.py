from scrapy.loader import ItemLoader
from scrapy import Spider

from ..items import EventItem
from .. import webdrivers
from .. import tools
from .. import paths


class TennisSpider(Spider):
    name = "tennis"
    start_urls = [paths.TENNIS_URL]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdrivers.chrome_driver()

    def parse(self, response, **kwargs):
        """Main scrapy logic is here"""
        content = tools.load_full_content(driver=self.driver, url=response.url)
        res = response.replace(body=content)
        rejected = []
        accepted = []
        tournaments = res.css('ms-event-group')
        all_events = res.xpath(paths.ALL_EVENTS_COUNT).get()

        for t in tournaments:
            for e in t.css('ms-event'):  # for e in events
                odds = e.css('ms-option-group')
                p1_odds = odds.xpath(paths.P1_ODDS).get()
                p2_odds = odds.xpath(paths.P2_ODDS).get()
                players = e.css('div.participant::text').getall()
                start_soon = e.css('ms-prematch-timer b::text').get()
                start_date = e.css('ms-prematch-timer::text').get()

                last_update = tools.convert_dt_to_str(tools.get_now_utc())
                ready_odds = [tools.odds_parser(x) for x in [p1_odds, p2_odds]]
                full_date = tools.date_parser(start_date, start_soon)
                p1, p2 = tools.players_parser(players)[1:3]
                e_name = tools.players_parser(players)[0]
                t_name = tools.t_name_parser(t.css('div div span::text').get())

                values = {'tournament': t_name,
                          'eventName': e_name,
                          'player1': p1,
                          'player2': p2,
                          'player1_odds': ready_odds[0],
                          'player2_odds': ready_odds[1],
                          'eventDate': full_date,
                          'lastUpdate': last_update}

                # If all values are complete save file,
                # otherwise append to rejected list for feedback
                loader = ItemLoader(item=EventItem(), selector=e)

                for k, v in values.items():
                    if v:
                        loader.add_value(k, v)
                    else:
                        rejected.append(values)
                        break
                if values not in rejected:
                    accepted.append(values)
                    yield loader.load_item()

        self.driver.close()
