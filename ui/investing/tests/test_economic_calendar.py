#!/usr/bin/python

import csv
import os

import datetime

from framework.ui.test_object import TestObject

from ui.investing.page_objects.modals.calendar_date_selection_modal import CalendarDateSelectionModal
from ui.investing.page_objects.modals.filter_country_selection_modal import FilterCountrySelectionModal
from ui.investing.page_objects.economic_calendar import EconomicCalendar
from ui.investing.page_objects.login import Login


class TestEconomicCalendar(TestObject):
    """
    This class contains tests for Economic Calendar page
    """
    __test__ = True

    """
    NOTE - don't care about:
    NZD - GlobalDairyTrade Price Index
    """

    def test_get_economic_calendar(self):
        """
        ui/investing/tests/test_economic_calendar.py::TestEconomicCalendar::test_get_economic_calendar
        """
        # init
        self.login = Login(self.driver)
        self.econ_cal = EconomicCalendar(self.driver)
        self.date_select_modal = CalendarDateSelectionModal(self.driver)

        # login
        url = self.configuration['serverUrl'] + '/login'
        self.driver.get(url)
        self.login.sign_in(
            email='',
            password=''
        )

        # navigate to econ calendar
        url = self.configuration['serverUrl'] + '/economic-calendar/'
        self.driver.get(url)

        # update calendar dates to last n days
        days_ago = 10
        self.econ_cal.click_btn_icon_calendar()
        today_dt = datetime.datetime.today()
        days_ago_dt = self.date_select_modal.calc_days_ago_from_today(today=today_dt, days_ago=days_ago)

        today_date_str = self.date_select_modal.fmt_dt_to_str(today_dt)
        start_date_str = self.date_select_modal.fmt_dt_to_str(days_ago_dt)

        # start_date_str = '02/01/2023'
        # today_date_str = '02/28/2023'

        self.date_select_modal.set_calendar_date(start_date= start_date_str, end_date=today_date_str)
        self.econ_cal.wait_for_econ_cal_spinner_invisible()

        data = self.econ_cal.get_table_data()

        folder_path = f'mation-out/{today_dt.year}-{today_dt.month}-{today_dt.day}_{days_ago}-days_ago'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        csv_file = open(f'{folder_path}/output.csv', 'w', newline='')
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(['Date', 'Time', 'Country', 'Sentiment', 'Event_Title', 'Actual', 'Forecast', 'Previous'])

        for date, values in data.items():
            for _, item in values.items():
                time = item['time']
                country = item['country']
                sentiment = item['sentiment']
                event_title = item['event_title']
                actual = item['actual']
                forecast = item['forecast']
                prev = item['prev']
                csv_writer.writerow([date, time, country, sentiment, event_title, actual, forecast, prev])

        csv_file.close()

    def test_get_economic_calendar_v2(self):
        """
        ui/investing/tests/test_economic_calendar.py::TestEconomicCalendar::test_get_economic_calendar_v2
        """
        # init
        self.login = Login(self.driver)
        self.econ_cal = EconomicCalendar(self.driver)
        self.date_select_modal = CalendarDateSelectionModal(self.driver)
        self.filter_country_select_modal = FilterCountrySelectionModal(self.driver)

        import configparser
        config = configparser.ConfigParser()
        config.read('configurations/config_secrets.ini')

        # login
        url = self.configuration['serverUrl'] + '/login'
        self.driver.get(url)
        self.login.sign_in(
            email=config.get('secrets', 'EMAIL'),
            password=config.get('secrets', 'PASSWORD')
        )

        # navigate to econ calendar
        url = self.configuration['serverUrl'] + '/economic-calendar/'
        self.driver.get(url)

        # update country filter
        self.filter_country_select_modal.click_btn_filter_country()
        self.filter_country_select_modal.wait_for_container_countries()
        self.filter_country_select_modal.click_btn_clear_selections()

        # countries = ['USA']
        countries = {
            "Australia": "AUD",
            "Canada": "CAD",
            "Europe": "EUR",
            "Germany": "EUR/GER",
            "Japan": "JPY",
            "New_Zealand": "NZD",
            "Switzerland": "CHF",
            "UK": "GBP",
            "USA": "USD"
        }
        for country in countries.keys():
            self.filter_country_select_modal.click_btn_country_selection(country)
        self.filter_country_select_modal.click_btn_apply()

        self.econ_cal.click_btn_icon_calendar()

        start_date_str = '05/25/2023'
        today_date_str = '05/26/2023'

        self.date_select_modal.set_calendar_date(start_date= start_date_str, end_date=today_date_str)
        self.econ_cal.wait_for_econ_cal_spinner_invisible()

        self.econ_cal.table_data_to_csv(countries)

    def test_get_tomorrows_economic_calendar(self):
        """
        ui/investing/tests/test_economic_calendar.py::TestEconomicCalendar::test_get_tomorrows_economic_calendar
        """
        # init
        self.economic_calendar = EconomicCalendar(self.driver)

        # get url
        url = self.configuration['ServerUrl'] + '/economic-calendar/'
        self.driver.get(url)

        # close popups
        self.economic_calendar.close_onload_popups()

        # set timezone
        self.economic_calendar.set_time("Pacific")

        # get todays economic calendar
        calendar = self.economic_calendar.get_tomorrows_economic_calendar()
        self.logger.debug(f'\n\nTomorrows Economic Calendar -> [{calendar}]')

    def test_get_this_weeks_economic_calendar(self):
        """
        ui/investing/tests/test_economic_calendar.py::TestEconomicCalendar::test_get_this_weeks_economic_calendar
        """
        # init
        # login
        url = self.configuration['serverUrl'] + '/login'
        self.driver.get(url)
        self.login = Login(self.driver)
        self.login.sign_in(
            email='econ.cal.mation@gmail.com',
            password='cujj7h-fehky9'
        )

        self.economic_calendar = EconomicCalendar(self.driver)

        # get url
        url = self.configuration['serverUrl'] + '/economic-calendar/'
        self.driver.get(url)

        # close popups
        # self.economic_calendar.close_onload_popups()

        # set timezone
        self.economic_calendar.set_time("Pacific")

        # get todays economic calendar
        calendar = self.economic_calendar.get_this_weeks_economic_calendar()
        self.logger.debug(f'\n\nTomorrows Economic Calendar -> [{calendar}]')