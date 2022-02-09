from selenium.webdriver.remote.webdriver import WebDriver
import time

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):

        for star_value in star_values:
            time.sleep(1)
            self.driver.find_element_by_xpath(f"//div[contains(text(),'{star_value} star')]").click()


    def sort_price_lowest_first(self):
        time.sleep(3)
        element = self.driver.find_element_by_css_selector(
            'li[data-id="price"]'
        )
        element.click()