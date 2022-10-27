# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProsettingsItem(scrapy.Item):
    # define the fields for your item here like:
    Player_Name = scrapy.Field()
    Player_Link = scrapy.Field()
    Page_Link = scrapy.Field()
    Mouse_Name = scrapy.Field()
    Mouse_Link = scrapy.Field()
    Monitor_Name = scrapy.Field()
    Monitor_Link = scrapy.Field()
    Mousepad_Name = scrapy.Field()
    Mousepad_Link = scrapy.Field()
    Keyboard_Name = scrapy.Field()
    Keyboard_Link = scrapy.Field()
    Headset_Name = scrapy.Field()
    Headset_Link = scrapy.Field()
    GPU_Name = scrapy.Field()
    GPU_Link = scrapy.Field()
    i = scrapy.Field()
    j = scrapy.Field()
    length = scrapy.Field()
    Record_create_dt = scrapy.Field()
    Type = scrapy.Field()
    Feed_code = scrapy.Field()
    Site = scrapy.Field()
    Source_country = scrapy.Field()
    Context_identifier = scrapy.Field()
    Record_create_by = scrapy.Field()
    Execution_id = scrapy.Field()
    pass
