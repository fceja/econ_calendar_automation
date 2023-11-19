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

        # define test props
        countries = {
            "Canada": "CAD",
            "USA": "USD"
        }
        email = self.config['testProperties']['investingAccountEmail']
        password = self.config['testProperties']['investingAccountPassowrd']

        calendar_start_date_str = '10/17/2023'
        calendar_today_date_str = '10/21/2023'

        # login
        url = self.config["testProperties"]["serverUrl"] + '/login'
        self.webdriver.get(url)
        self.login.sign_in(email = email, password = password)

        # navigate to econ calendar
        url = self.config["testProperties"]['serverUrl'] + '/economic-calendar/'
        self.webdriver.get(url)

        # update country filter
        self.filter_country_select_modal.click_btn_filter_country()
        self.filter_country_select_modal.wait_for_container_countries()
        self.filter_country_select_modal.click_btn_clear_selections()

        for country in countries.keys():
            self.filter_country_select_modal.click_btn_country_selection(
                country)
        self.filter_country_select_modal.click_btn_apply()

        self.econ_cal.click_btn_icon_calendar()

        self.date_select_modal.set_calendar_date(
            start_date=calendar_start_date_str, end_date=calendar_today_date_str)
        self.econ_cal.wait_for_econ_cal_spinner_invisible()

        self.econ_cal.scroll_to_last_row()
        self.econ_cal.scroll_to_first_row()

        self.econ_cal.table_data_to_csv(
            countries, calendar_start_date_str, calendar_today_date_str)
