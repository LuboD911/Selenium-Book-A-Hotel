from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements_by_xpath(
            "//div[@data-testid='property-card']"
        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:

            # Pulling the hotel name
            hotel_name = deal_box.find_element_by_xpath(
                ".//div[@data-testid='title']"
            ).text.strip()

            hotel_price = deal_box.find_element_by_xpath(
                "(.//div[@data-testid='price-and-discounted-price']/span)[last()]"
            ).text.strip()


            try:
                hotel_score = deal_box.find_element_by_xpath(
                    ".//div[contains(@aria-label,'Scored')]"
                ).text.strip()

            except:
                hotel_score = 'No info'

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        return collection