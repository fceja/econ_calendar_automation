#!/usr/bin/python

import datetime

from framework.ui.page_object import PageObject

class CalendarDateSelectionModal(PageObject):
    """
    This class contains interactions for calendar date selection modal
    on /economic-calendar pageobject
    """

    # region clickers
    def click_btn_apply(self):
        self._wait_for_element_visible('btn_apply')
        self._click_element('btn_apply')
    # endregion clickers

    # region Setters
    def set_start_date(self, start_date):
        self._wait_for_element_visible('input_start_date')
        self._clear_element_data('input_start_date')
        self._set_element_value('input_start_date', start_date)

    def set_end_date(self, end_date):
        self._wait_for_element_visible('input_end_date')
        self._clear_element_data('input_end_date')
        self._set_element_value('input_end_date', end_date)

    def set_calendar_date(self, start_date, end_date):
        """
        start_date: str - how many days ago start date should be
        end_date: datetime

        note: will need to update for settin different end_date
        """
        self.set_start_date(start_date)
        self.set_end_date(end_date)

        self.click_btn_apply()
    # endregion Setters

    # region Waiters
    def wait_for_date_picker_invisible(self):
        self._wait_for_dynamic_element_visible('ui-datepicker')
        self._wait_for_dynamic_element_invisible('ui-datepicker')
    # endregion Waiters

    # region Macros
    def fmt_dt_to_str(self, dt_obj):
        return f'{dt_obj.month}/{dt_obj.day}/{dt_obj.year}'

    def calc_days_ago_from_today(self, today, days_ago):
        start_date_dt = today - datetime.timedelta(days=days_ago)
        return start_date_dt
    # endregion Macros
