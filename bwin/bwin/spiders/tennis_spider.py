from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from scrapy.loader import ItemLoader
from scrapy import Spider

from ..items import EventItem
from .. import tools
from .. import paths

# Selenium webdrive settings
options = ChromeOptions()
options.add_argument("--headless")
# options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)


class TennisSpider(Spider):
    name = "tennis"
    start_urls = [paths.TENNIS_URL]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize selenium webdriver through https://pypi.org/project/webdriver-manager/
        self.driver = driver

    def parse(self, response, **kwargs):
        """Main scrapy logic is here"""
        content = tools.load_full_content(driver=self.driver, url=response.url)
        res = response.replace(body=content)
        rejected = []
        accepted = []
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

                values = {'tournament': t_name,
                          'eventName': e_name,
                          'player1': p1,
                          'player2': p2,
                          'player1_odds': ready_odds[0],
                          'player2_odds': ready_odds[1],
                          'eventDate': full_date,
                          'lastUpdate': last_update}

                for k, v in values.items():
                    if v:
                        loader.add_value(k, v)

                    else:
                        rejected.append(values)
                        yield print(values)
                        break
                if values not in rejected:
                    accepted.append(values)
                    yield loader.load_item()

        yield print(f"ACCEPTED: {len(accepted)} | REJECTED {len(rejected)}")

        self.driver.close()
