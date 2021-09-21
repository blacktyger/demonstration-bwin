from scrapy.loader import ItemLoader
from scrapy import Spider

from bwin.items import EventItem
from bwin import webdrivers
from bwin import tools
from bwin import paths


class TennisSpider(Spider):
    name = "tennis"
    start_urls = [paths.TENNIS_URL]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.driver = webdrivers.firefox_driver()
        self.driver = webdrivers.chrome_driver()

    def parse(self, response, **kwargs):
        """Main scrapy logic is here"""
        content = tools.load_full_content(driver=self.driver, url=response.url)
        res = response.replace(body=content)
        rejected = []
        completed = []
        tournaments = res.css('ms-event-group')

        for t in tournaments:
            for e in t.css('ms-event'):  # for e in events
                odds = e.css('ms-option-group')
                p1_odds = odds.xpath(paths.P1_ODDS).get()
                p2_odds = odds.xpath(paths.P2_ODDS).get()
                players = e.css('div.participant::text').getall()
                start_soon = e.css('ms-prematch-timer b::text').get()
                start_date = e.css('ms-prematch-timer::text').get()

                # Parsing collected data
                last_update = tools.convert_dt_to_str(tools.get_now_utc())
                ready_odds = [tools.odds_parser(x) for x in [p1_odds, p2_odds]]
                full_date = tools.date_parser(start_date, start_soon)
                t_name = tools.t_name_parser(t.css('div div span::text').get())
                e_name, p1, p2 = tools.players_parser(players)

                event = {'tournament': t_name,
                         'eventName': e_name,
                         'player1': p1,
                         'player2': p2,
                         'player1_odds': ready_odds[0],
                         'player2_odds': ready_odds[1],
                         'eventDate': full_date,
                         'lastUpdate': last_update}

                # If all values are complete save to file,
                # otherwise append to rejected list for feedback
                if (last_update and ready_odds and
                    full_date and t_name and e_name) is not None:
                    loader = ItemLoader(item=EventItem(), selector=e)
                    completed.append(event)
                    for k, v in event.items():
                        loader.add_value(k, v)
                        yield loader.load_item()
                else:
                    rejected.append(event)

        # Compare number of events on page vs scrapped events
        all_events = res.xpath(paths.ALL_EVENTS_COUNT).get()
        outrights = res.xpath(paths.OUTRIGHTS).get()
        specials = res.xpath(paths.SPECIALS).get()
        to_scrape = int(all_events) - (int(outrights) + int(specials))

        self.crawler.stats.set_value('to_scrape', to_scrape)
        self.crawler.stats.set_value('rejected', len(rejected))
        self.crawler.stats.set_value('completed', len(completed))
        self.driver.close()
