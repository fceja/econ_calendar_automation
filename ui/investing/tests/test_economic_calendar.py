#!/usr/bin/python

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

    def test_get_economic_calendar(self):
        """
        ui/investing/tests/test_economic_calendar.py::TestEconomicCalendar::test_get_economic_calendar
        """
        # init
        self.login = Login(self.webdriver)
        self.econ_cal = EconomicCalendar(self.webdriver)
        self.date_select_modal = CalendarDateSelectionModal(self.webdriver)
        self.filter_country_select_modal = FilterCountrySelectionModal(
            self.webdriver)

        import configparser
        config = configparser.ConfigParser()
        config.read('configurations/config_secrets.ini')

        # login
        url = self.config["testProperties"]["serverUrl"] + '/login'
        self.webdriver.get(url)
        self.login.sign_in(
            email=config.get('secrets', 'EMAIL'),
            password=config.get('secrets', 'PASSWORD')
        )

        # navigate to econ calendar
        url = self.config["testProperties"]['serverUrl'] + '/economic-calendar/'
        self.webdriver.get(url)

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
            self.filter_country_select_modal.click_btn_country_selection(
                country)
        self.filter_country_select_modal.click_btn_apply()

        self.econ_cal.click_btn_icon_calendar()

        start_date_str = '12/15/2022'
        today_date_str = '12/16/2022'

        self.date_select_modal.set_calendar_date(
            start_date=start_date_str, end_date=today_date_str)
        self.econ_cal.wait_for_econ_cal_spinner_invisible()

        self.econ_cal.scroll_to_last_row()
        self.econ_cal.scroll_to_first_row()

        self.econ_cal.table_data_to_csv(
            countries, start_date_str, today_date_str)
