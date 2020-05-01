# -*- coding: utf-8 -*-
import scrapy
import logging
import SkalTrial.items
import re
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from asyncio.tasks import sleep
from SkalTrial.items import WhiskeyItem

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

        #Regular Expression to find the value in the parantheses ^.*?\([^\d]*(\d+)[^\d]*\).*$
        pattern = "^.*?\([^\d]*(\d+)[^\d]*\).*$"      

        #Converting the second page source into selectors
        second_screen_source = driver.page_source
        second_screen = Selector(text=second_screen_source)
        logging.info("Second screen source has been converted into an Selector")

        #Waiting till the page gets loaded completely by checking the whether the loader button is present at the bottom.
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR,"#main > div:nth-child(2) > div > div > section > div.controls.cmp-tab-container > ul > li.all-hits.selected > a > span:nth-child(3)"))
            WebDriverWait(driver, 25).until(element_present)
        except TimeoutException:
            logging.error("Page doesn't load, time out error has been occurred")
            raise TimeoutException

        #Checking the total count
        count = second_screen.css("#main > div:nth-child(2) > div > div > section > div.controls.cmp-tab-container > ul > li.all-hits.selected > a > span:nth-child(3)::text").get()
        res = re.findall(pattern, count)
        cnt = res[0]
        logging.info("Total Number of products present "+cnt)

        #pagination for loading the complete website
        # c=0
        while(True):
            try:
                show_button = driver.find_element_by_css_selector(".cmp-btn--show-more")
                actions1 = ActionChains(driver)
                actions1.move_to_element(show_button)
                actions1.click(show_button)
                actions1.perform()
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR,".cmp-btn--show-more"))
                WebDriverWait(driver, 1200,60).until(element_present)
                # c=c+1
                # driver.save_screenshot("fourth"+str(c)+".png")
                second_screen_source = driver.page_source
                second_screen = Selector(text=second_screen_source)
            except NoSuchElementException:
                logging.info("No such element exception breaking the while loop")
                break
            except:
                break
        
        # driver.save_screenshot("fourth.png")

        #Collecting all the data from the container
        products = second_screen.css(".result-list>.elm-product-list-item-full>a[href]").getall()
        logging.info("Got all the containers in the page and looping through the products and yielding the values")
        for p1 in products:
            p = Selector(text=p1)
            # yield{
            Item = WhiskeyItem()
            Item['name1']=p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-left>.product-name-bold::text").get()
            Item['name2']=p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-left>.product-name-thin::text").get()
            Item['price']=p.css(".elm-product-list-item-full-info>.row-container>.row-1>.col-right::text").get().strip().replace(":-","").replace(":-*","")
            Item['bottle_text']=p.css(".elm-product-list-item-full-info>.row-container>.row-2>.col-right>.info>.bottle-text-short::text").get()
            Item['quantity']=p.css(".elm-product-list-item-full-info>.row-container>.row-2>.col-right>.info>span.ng-binding:nth-child(2)::text").get()
            Item['description1']=p.css(".elm-product-list-item-full-info > div.row-container.clearfix > div.row-3 > div > span::text").get()
            Item['description2']=p.css(".elm-product-list-item-full-info > div.row-container.clearfix > div.row-4 > div > span::text").get()
            # Item['extra_notification']=p.css("").get()
            # #main > .elm-product-list-item-full-info > div.row-container.clearfix > div.row-3 > div > span
            #main > div:nth-child(2) > div > div > section > div.results.full-assortment > ul > li:nth-child(1) > a > div.elm-product-list-item-full-info > div.row-container.clearfix > div.row-4 > div > span
            # }
            logging.info(Item['price'])
            yield Item
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

        
