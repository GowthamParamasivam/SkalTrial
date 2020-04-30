# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains

class SystembolagetSpider(scrapy.Spider):
    name = 'systembolaget'
    allowed_domains = ['www.systembolaget.com']
    start_urls = ['https://www.systembolaget.se/sok-dryck/?searchquery=Whisky']

    def start_requests(self):
        start_urls = ['https://www.systembolaget.se/sok-dryck/?searchquery=Whisky']
        for url in start_urls:
            yield SeleniumRequest(url=url, screenshot=True,callback=self.parse)


    def parse(self, response):
        #image for the first request 
        first_image = response.meta['screenshot']
        with open('first_request.png','wb') as f:
            f.write(first_image)
            logging.info("First Image of the First Request Has been saved with name first_request.png")
        
        #Checking if the age check constraint is asked
        logging.info("Checking whether the age check is asked")
        driver = response.meta['driver']
        above20 = driver.find_element_by_css_selector("#modal-agecheck>.modal-table>.modal-row>.modal-cell>.content-wrapper>.content>.actions>.action:nth-child(2)")
        if above20 is not None:
            logging.info("Age check is present and trying to pass the age check")
            actions = ActionChains(driver)
            actions.move_to_element(above20)
            actions.click(above20)
            actions.perform()
            logging.info("Age check has been passed")

        driver.save_screenshot("second_image.png")
        logging.info("Second image after the age check has been saved in name second_image.png")

        #Converting the second page source into selectors
        second_screen_source = driver.page_source
        second_screen = Selector(text=second_screen_source)
        logging.info("Second screen source has been converted into an Selector")

        products = second_screen.css(".result-list>.elm-product-list-item-full>a[href]").getall()
        logging.info("Got all the containers in the page and looping through the products and yielding the values")
        for p1 in products:
            p = Selector(text=p1)
            yield{
                'product_name':p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-left>.product-name-bold::text").get(),
                'product_name2':p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-left>.product-name-thin::text").get(),
                'product_price':p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-right::text").get(),
                'product_bottle_text':p.css(".elm-product-list-item-full-info>.row-container>.row-2>.col-right>.info>.bottle-text-short::text").get(),
                'product_quantity':p.css(".elm-product-list-item-full-info>.row-container>.row-2>.col-right>.info>span.ng-binding:nth-child(2)::text").get()
            }
        logging.info("Yielding has been done successfully")
        pass


        #todo pagination pending
        #data source pipelines
        #structured data objects





###################################################################################################
        # for i in r:
        #     print(i)
        #     with open("text1.txt", 'w') as fin:
        #         print(fin.write(i))
        #     break

        
