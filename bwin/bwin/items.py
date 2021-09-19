from itemloaders.processors import TakeFirst
from scrapy import Item, Field


class EventItem(Item):
    tournament = Field(output_processor=TakeFirst())
    eventName = Field(output_processor=TakeFirst())
    player1 = Field(output_processor=TakeFirst())
    player2 = Field(output_processor=TakeFirst())
    player1_odds = Field(output_processor=TakeFirst())
    player2_odds = Field(output_processor=TakeFirst())
    eventDate = Field(output_processor=TakeFirst())
    lastUpdate = Field(output_processor=TakeFirst())

