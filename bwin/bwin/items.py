# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy import Item, Field


class EventItem(Item):
    tournament = Field(output_processor=TakeFirst())
    eventName = Field(output_processor=TakeFirst())
    player1 = Field(output_processor=TakeFirst())
    player2 = Field(output_processor=TakeFirst())
    # TODO: odds logic and  parser
    player1_odds = Field(output_processor=TakeFirst())
    player2_odds = Field(output_processor=TakeFirst())
    # TODO: datetime parser
    eventDate = Field()
    lastUpdate = Field(output_processor=TakeFirst())

