from abc import ABC
from time import sleep
from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog
import pandas as pd


class PropertiesSpider(Spider, ABC):
    name = 'properties'
    allowed_domains = ['gwinnettassessor.manatron.com']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.driver = webdriver.Chrome('/Users/wenzeljoe/CondaProjects/chromedriver')

    def start_requests(self):
        global df
        import_file_path = filedialog.askopenfilename()
        df = pd.read_excel(import_file_path)
        parcels = df.values.T[0].tolist()

        for parcel in parcels:
            self.driver.get('http://gwinnettassessor.manatron.com/IWantTo/PropertyGISSearch.aspx')

            search_bar = self.driver.find_element_by_xpath("//table/tbody/tr/td/div/input")
            search_bar.send_keys(parcel)
            sleep(3)

            button = self.driver.find_element_by_xpath("//button/span")
            button.click()

            sel = Selector(text=self.driver.page_source)
            properties = sel.xpath("//ul[2]/li/a/@href").extract()
            sleep(3)
            for property in properties:
                sleep(3)
                url = 'http://gwinnettassessor.manatron.com/IWantTo/PropertyGISSearch.aspx' + property
                yield SeleniumRequest(url=url,
                                      callback=self.parse_property,
                                      wait_time=10,
                                      wait_until=EC.presence_of_element_located)
        self.driver.close()

    def parse_property(self, response):
        data = {}
        data['parcel_id'] = response.selector.xpath(
            '//table[@class="ui-widget-content ui-table generalinfo"]/tbody/tr[2]/td/text()').extract_first()
        data['address'] = response.selector.xpath(
            '//table[@class="ui-widget-content ui-table generalinfo"]/tbody/tr[4]/td/text()').extract_first()
        data['name'] = response.selector.xpath(
            '//table[@class="ui-widget-content ui-table generalinfo"]/tbody/tr/td/text()').extract_first()
        data['land_value'] = response.xpath('//*[@title="Land Val"]/following-sibling::td/text()').extract_first()
        data['total_appr'] = response.xpath('//*[@title="Total Appr"]/following-sibling::td/text()').extract_first()

        yield data


