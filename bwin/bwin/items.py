# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy import Item, Field


def extract_name(text):
    return text.split('-')[0].strip()


class TournamentItem(Item):
    event = Field()
