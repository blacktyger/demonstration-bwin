import time

from scrapy.loader import ItemLoader
import scrapy
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from ..items import TournamentItem

driver = webdriver.Chrome(ChromeDriverManager().install())
tennis_url = 'https://sports.bwin.com/en/sports/tennis-5/betting'

class TennisSpider(scrapy.Spider):
    name = "tennis"
    start_urls = [tennis_url]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def parse(self, response, **kwargs):
        self.driver.get(response.url)
        self.driver.implicitly_wait(5)
        scroll = self.driver.find_element_by_xpath('//*[@id="main-view"]/ms-fixture-list/div/div/div/div[2]/div')
        popup = self.driver.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]')
        popup_btn = self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
        actions = ActionChains(self.driver)

        scroll_num = 5

        while scroll_num:
            try:
                if popup.is_displayed():
                    popup_btn.click()
                actions.move_to_element(scroll).perform()
                scroll_num -= 1
                time.sleep(2)
            except Exception:
                if popup.is_displayed():
                    popup_btn.click()
                scroll_num -= 1
                time.sleep(2)
                continue
        time.sleep(5)
        res = response.replace(body=self.driver.page_source)

        events = res.css('ms-event')

        for e in events:
            loader = ItemLoader(item=TournamentItem(), selector=e)
            players = e.css('div.participant::text').getall()
            loader.add_value('event', players)
            yield loader.load_item()

        self.driver.close()
