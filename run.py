import time

from booking.booking import Booking


with Booking() as bot:
    bot.land_first_page()
    time.sleep(4)
    bot.accept_coockies()
    bot.change_currency(currency='USD')
    # bot.select_place_to_go(input("Where you want to go ?"))
    bot.select_place_to_go("Milan")
    #DD-MM-YYYY format
    # bot.select_dates(check_in_date=input("What is the check in date ? YYYY-MM-DD format:"),
    #                  check_out_date=input("What is the check out date ? YYYY-MM-DD format:"))
    bot.select_dates(check_in_date="2022-04-16",
                     check_out_date="2022-04-19")
    bot.open_to_choose_adults_and_rooms()
    bot.select_adults(10)
    bot.select_rooms(4)
    bot.click_search()
    bot.apply_filtrations()
    time.sleep(8)
    bot.report_results()