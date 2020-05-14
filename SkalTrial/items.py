# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkaltrialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# class Drinks(scrapy.Item):
#     # define the fields for your item here like:
#     _id = scrapy.Field()
#     name1 = scrapy.Field()
#     name2 = scrapy.Field()
#     quantity = scrapy.Field()
#     price = scrapy.Field()
#     bottle_text = scrapy.Field()
#     description1 = scrapy.Field()
#     description2 = scrapy.Field()
#     availability = scrapy.Field()
#     sales_starts_at = scrapy.Field()
#     category = scrapy.Field()
#     scrapped_on = scrapy.Field(serializer=str)
#     pass

class DrinksLatest(scrapy.Item):
    _id = scrapy.Field()
    ProductId = scrapy.Field()
    ProductNumber = scrapy.Field()
    ProductNameBold = scrapy.Field()
    ProductNameThin = scrapy.Field()
    Category = scrapy.Field()
    ProductNameBold = scrapy.Field()
    ProductNumberShort = scrapy.Field()
    ProducerName = scrapy.Field()
    BottleTextShort = scrapy.Field()
    Volume = scrapy.Field()
    Price = scrapy.Field()
    Country = scrapy.Field()
    SubCategory = scrapy.Field()
    Type = scrapy.Field()
    BeverageDescriptionShort = scrapy.Field()
    Usage = scrapy.Field()
    Taste = scrapy.Field()
    SellStartText = scrapy.Field()
    Availability = scrapy.Field()
    VolumeText = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    Store = scrapy.Field()
    ScrappedDate = scrapy.Field()

class Store(scrapy.Item):
    StoreNumber = scrapy.Field()
    SiteId = scrapy.Field()
    Alias = scrapy.Field()
    StreetAddress = scrapy.Field()
    PostalCode = scrapy.Field()
    City = scrapy.Field()
    Phone = scrapy.Field()
    County = scrapy.Field()
    IsTastingStore = scrapy.Field()
    IsActiveForAgentOrder = scrapy.Field()
    IsStore = scrapy.Field()
    IsDepot = scrapy.Field()
    IsAgent = scrapy.Field()
    OpeningHours = scrapy.Field()
    DeliverySchedule = scrapy.Field()
    PickupHours = scrapy.Field()
    SiteUrl = scrapy.Field()
    OpeningHoursTodayText = scrapy.Field()
    Shelf = scrapy.Field()
    Stock = scrapy.Field()
    SectionLabel = scrapy.Field()
    ShelfLabel = scrapy.Field()
    StockLabel = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    Rt90x = scrapy.Field()
    Rt90y = scrapy.Field()
    StoreTimingToday = scrapy.Field()
    NotYetSaleStarted = scrapy.Field()

class StoreOpen(scrapy.Item):
    _id = scrapy.Field()
    Alias = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    County = scrapy.Field()
    Lat = scrapy.Field()
    Long = scrapy.Field()
    OpenToday = scrapy.Field()
    SiteId = scrapy.Field()
    IsAgent = scrapy.Field()
    IsTastingStore = scrapy.Field()