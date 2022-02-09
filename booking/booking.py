import time

import booking.constants as const
import os
from selenium import webdriver
from prettytable import PrettyTable
from datetime import date

from booking.book_filtration import BookingFiltration
from booking.book_report import BookingReport


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\Selenium Drivers",
                 teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def accept_coockies(self):
        try:
            self.find_element_by_xpath("//button[contains(text(),'Accept')]").click()
            print("Cookies accepted")
        except:
            print('Cookies msg not found')

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()


    def select_place_to_go(self, place_to_go):
        search_field = self.find_element_by_id('ss')
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element_by_css_selector(
            'li[data-i="0"]'
        )
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):

        if check_in_date < str(date.today()) or check_out_date < check_in_date:
            self.quit()
            raise ValueError("Please enter a correct date")

        clicked = False
        while True:

            if not clicked:
                try:
                    self.find_element_by_css_selector(f'td[data-date="{check_in_date}"]').click()
                    clicked = True
                except:
                    self.find_element_by_xpath("//div[contains(@class,'next')]").click()
                    continue

            try:
                self.find_element_by_css_selector(f'td[data-date="{check_out_date}"]').click()
                break
            except:
                self.find_element_by_xpath("//div[contains(@class,'next')]").click()



    def open_to_choose_adults_and_rooms(self):
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()


    def select_adults(self, count=1):

        value = int(self.find_element_by_id('group_adults').get_attribute('value'))

        while value != count:

            if value > count:
                self.find_element_by_css_selector("button[aria-label='Decrease number of Adults']").click()
                value -= 1
            elif value < count:
                self.find_element_by_css_selector("button[aria-label='Increase number of Adults']").click()
                value += 1


    def select_rooms(self, count=1):

        value = int(self.find_element_by_id('no_rooms').get_attribute('value'))

        while value != count:

            if value > count:
                self.find_element_by_css_selector("button[aria-label='Decrease number of Rooms']").click()
                value -= 1
            elif value < count:
                self.find_element_by_css_selector("button[aria-label='Increase number of Rooms']").click()
                value += 1


    def click_search(self):
        search_button = self.find_element_by_css_selector(
            'button[type="submit"]'
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)

        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element_by_css_selector(
            "[data-block-id='hotel_list']"
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        
        print(table)