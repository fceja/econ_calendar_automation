#!/usr/bin/python

from framework.ui.page_object import PageObject

class Login(PageObject):
    """
    This class contains Login Page interactions
    """

    def __init__(self, driver):
        super(Login, self).__init__(driver)

    # region waiters
    def wait_input_email_visible(self):
        self._wait_for_element_visible('input_email')
    # endregion waiters

    # region macros
    def sign_in(self, email, password):
        self.wait_input_email_visible()

        self._set_element_value('input_email', email)
        self._set_element_value('input_password', password)

        self._click_element('btn_sign_in')
    # endregion macros