#!/usr/bin/python

import inspect
import json
import os
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from framework.utils.logger import Logger
from framework.utils.config_parser import ConfigParser


class PageObject(object):
    """
    Base class for automation page objects.
    Contains WebDriver page interactions.

    Helpful Reading:
        - https://selenium-python.readthedocs.io/api.html
        - https://www.selenium.dev/documentation/webdriver/
        - https://www.selenium.dev/documentation/webdriver/elements/
        - https://www.selenium.dev/documentation/webdriver/elements/locators/
        - https://www.selenium.dev/documentation/webdriver/elements/finders/
        - https://www.selenium.dev/documentation/webdriver/elements/interactions/
        - https://www.selenium.dev/documentation/webdriver/elements/information/
        - https://www.selenium.dev/documentation/webdriver/interactions/

    """
    def __init__(self, webdriver):
        """
        :param webdriver: WebDriver instance
        """
        self.logger = Logger().get_logger()

        self.load_json_locator_data()
        self.config = ConfigParser()

        # webdriver setup
        self.driver = webdriver

        self.wait_time = int(self.config['webDriver']['webdriverImplicitWait'])
        self.max_wait_time = int(self.config['webDriver']['maximumWaitTime'])

    def load_json_locator_data(self):
        """
        Attempts to load json file with locator data for initialized page object.
        Example:
            - page object: homePage.py
            - locator file: homepage.json
        """
        json_locator_file_path = os.path.abspath(inspect.getfile(self.__class__)).replace('.py', '.json')
        self.logger.debug(json_locator_file_path)
        if os.path.isfile(json_locator_file_path):
            with open(json_locator_file_path) as json_file:
                self.locator_json = json.load(json_file)

    def _pause(wait=0):
        """
        :param wait: time to wait.
        """
        time.sleep(wait)

    # region Clickers
    def _double_click_element(self, json_key):
        """
        Double clicks DOM element, indicated by json key

        :param json_key: locator json key
        """
        self.logger.debug("_double_click_element")
        element = self._get_element(json_key)
        ActionChains(self.driver) \
            .double_click(element) \
            .perform()

    def _click_element(self, json_key):
        """
        Clicks DOM element, indicated by json key

        :param json_key: locator json key
        """
        self.logger.debug("_click_element")
        element = self._get_element(json_key)
        try:
            element.click()
        except:
            element.click()

    def _click_dynamic_element(self, json_key, *args):
        """
        Clicks DOM element, indicated by json key

        :param json_key: locator json key to dynamically format
        :param args: arguments to format json key
        """
        self.logger.debug("_click_dynamic_element")
        element = self._get_dynamic_element(json_key, *args)

        element.click()

    def _action_click_element(self, json_key):
        """
        Clicks DOM element, indicated by json key
        Uses ActionChains

        :param json_key: locator json key
        """
        self.logger.debug("_action_click_element")
        element = self._get_element(json_key)

        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def _action_dynamic_click_element(self, json_key, *args):
        """
        Clicks DOM element, indicated by json key
        Uses ActionChanins

        :param json_key: locator json key to dynamically format
        :param args: arguments to format json key
        """
        self.logger.debug("_action_dynamic_click_element")
        element = self._get_dynamic_element(json_key, *args)

        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()
    # endregion Clickers

    # region Getters
    def _get_dynamic_element(self, json_key, *args):
        """
        Retrieves DOM element(s), indicated by json key

        :param json_key: locator json key to dynamically format
        :param args: arguments to format json key
        :return: html element as WebElement

        """
        self.logger.debug("_get_dynamic_element")
        by, locator = self._get_dynamic_locator(json_key, *args)
        return self.driver.find_element(by, locator)

    def _get_element(self, json_key):
        """
        Retrieves DOM element, indicated by json key

        :param json_key: locator json key
        :return: html element as WebElement
        """
        self.logger.debug("_get_element")
        by, locator = self._get_locator(json_key)
        return self.driver.find_element(by, locator)

    def _get_locator(self, json_key):
        """
        Get the locator json key pair

        https://www.selenium.dev/documentation/webdriver/elements/locators/
        - locatorType
            - class name
            - css selector
            - name
            - id
            - xpath
        - locator
            - locator value

        :param json_key: locator json key
        :return: locator tuple

        """
        key_pair_value = self.locator_json[json_key]

        locator_type = key_pair_value['locator_type']
        locator_value = key_pair_value['locator']
        self.logger.debug(f"locator_type: {locator_type} locator: {locator_value}")

        return locator_type, locator_value

    def _get_dynamic_locator(self, json_key, *args):
        """
        Retrieves DOM element, indicated by json key

        :param json_key: locator json key
        :param args: arguments to format json key
        :return: locator tuple

        """
        key_pair_value = self.locator_json[json_key]

        locator_type = key_pair_value['locator_type']
        locator_value = key_pair_value['locator'].format(*args)

        self.logger.debug(f"locator_type: {locator_type} locator: {locator_value}")

        return locator_type, locator_value

    def _get_element_text(self, json_key):
        """
        Retrieves DOM element text, indicated by json key

        :param json_key: locator json key
        :return: string

        """
        element = self._get_element(json_key)
        text = element.text.strip()

        self.logger.debug('text: "%s"' % text)
        return text

    def _get_elements_text(self, json_key):
        """
        Retrieves DOM element(s) text, indicated by json key

        :param json_key: locator json key
        :return: WebElement list

        """
        strings = []
        elements = self._get_elements(json_key)
        for element in elements:
            strings.append(element.text.strip())

        self.logger.debug(strings)
        return strings

    def _get_dynamic_elements_text(self, json_key, *args):
        """
        Retrieves DOM element(s) text, indicated by json key

        :param json_key: locator json key
        :param args: arguments to format json key
        :return: string

        """
        strings = []
        elements = self._get_dynamic_elements(json_key, *args)
        for element in elements:
            strings.append(element.text.strip())
        self.logger.debug('strings: ' + str(strings))
        return strings

    def _get_dynamic_element_text(self, json_key, *args):
        """
        Retrieves DOM element text, indicated by json key

        :param json_key: locator json key
        :param args: arguments to format json key
        :return: string

        """
        element = self._get_dynamic_element(json_key, *args)
        text = element.text.strip()
        self.logger.debug('text: ' + str(text))
        return text

    def _get_elements(self, json_key):
        """
        Retrieves DOM element(s), indicated by json key

        :param json_key: locator json key
        :return: WebElement list
        """
        self.logger.debug("_get_elements")
        by, locator = self._get_locator(json_key)
        return self.driver.find_elements(by, locator)

    def _get_dynamic_elements(self, json_key, *args):
        """
        Retrieves DOM element(s), indicated by json key

        :param json_key: locator json key
        :param args: arguments to format json key
        :return: WebElement list
        """
        self.logger.debug("_get_dynamic_elements")
        by, locator = self._get_dynamic_locator(json_key, *args)
        return self.driver.find_elements(by, locator)

    def _get_elements_attribute(self, json_key, attr):
        """
        Retrieves DOM element(s) attribute value, indicated by json key

        :param json_key: locator json key
        :param attr: attribute to retrieve
        :return: list of strings

        """
        elements = self._get_elements(json_key)
        attributes = []
        for e in elements:
            value = e.get_attribute(attr)
            if value:
                value = value.strip()
            attributes.append(value)

        return attributes

    def _get_dynamic_elements_attribute(self, json_key, attr, *args):
        """
        Retrieves DOM element(s) attribute value, indicated by json key

        :param json_key: locator json key
        :param attr: attribute to retrieve
        :param args: arguments to format json key
        :return: list of strings

        """
        elements = self._get_dynamic_elements(json_key, *args)
        attributes = []
        for e in elements:
            value = e.get_attribute(attr)
            if value:
                value = value.strip()
            attributes.append(value)

        return attributes

    def _get_element_attribute(self, json_key, attr):
        """
        Retrieves DOM element attribute value, indicated by json key

        :param json_key: locator json key
        :param attr: attribute to retrieve
        :return: list of strings

        """
        self.logger.debug("_get_element_attribute " + str(attr))
        value = self._get_element(json_key).get_attribute(attr)
        if value:
            value = value.strip()
        self.logger.debug(str(value))
        return value

    def _get_dynamic_element_attribute(self, json_key, attr, *args):
        """
        Retrieves DOM element attribute value, indicated by json key

        :param json_key: locator json key
        :param attr: attribute to retrieve
        :param args: arguments to format json key
        :return: list of string

        """
        self.logger.debug("_get_dynamic_element_attribute " + str(attr))
        value = self._get_dynamic_element(json_key, *args).get_attribute(attr)
        if value:
            value = value.strip()
        self.logger.debug(str(value))
        return value
    # endregion Getters

    # region Setters
    def __send_keys(self, element, value):
        """
        Sends keystrokes to DOM elements

        :param element: WebElemet
        :param value: string value to send
        """
        self.logger.debug("__send_keys " + str(value))
        element.send_keys(str(value))

    def _set_element_value(self, json_key, value):
        """
        Set DOM input element value

        :param json_key: locator json key
        :param value: string value to set
        """
        element = self._get_element(json_key)
        if not value:
            element.click()
            text = element.get_attribute('value')
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.END).perform()
            for i in range(len(text)):
                actions.send_keys(Keys.BACKSPACE).perform()
        else:
            self.__send_keys(element, value)

    def _set_dynamic_element_value(self, json_key, value, *args):
        """
        Set DOM input element value

        :param json_key: locator json key
        :param value: value to set
        """
        element = self._get_dynamic_element(json_key, *args)
        self.__send_keys(element, value)
    # endregion Setters

    # region Wait
    def _wait_for_element_invisible(self, json_key, wait_time=None):
        return self._wait(EC.invisibility_of_element, json_key, wait_time=wait_time)

    def _wait_for_element_visible(self, json_key, wait_time=None):
        return self._wait(EC.visibility_of_element_located, json_key, wait_time=wait_time)

    def _wait_for_element_selected(self, json_key, wait_time=None):
        return self._wait(EC.element_located_to_be_selected, json_key, wait_time=wait_time)

    def _wait_for_element_present(self, json_key, wait_time=None):
        return self._wait(EC.presence_of_element_located, json_key, wait_time=wait_time)

    def _wait_for_element_clickable(self, json_key, wait_time=None):
        return self._wait(EC.element_to_be_clickable, json_key, wait_time=wait_time)

    def _wait_for_dynamic_element_invisible(self, json_key, *args, wait_time=None):
        return self.dynamic_wait(EC.invisibility_of_element, json_key, *args, wait_time=wait_time)

    def _wait_for_dynamic_element_visible(self, json_key, *args, wait_time=None):
        return self.dynamic_wait(EC.visibility_of_element_located, json_key, *args, wait_time=wait_time)

    def _wait_for_dynamic_element_selected(self, json_key, *args, wait_time=None):
        return self.dynamic_wait(EC.element_located_to_be_selected, json_key, *args, wait_time=wait_time)

    def _wait_for_dynamic_element_present(self, json_key, *args, wait_time=None):
        return self.dynamic_wait(EC.presence_of_element_located, json_key, *args, wait_time=wait_time)

    def _wait_for_dynamic_element_clickable(self, json_key, *args, wait_time=None):
        return self.dynamic_wait(EC.element_to_be_clickable, json_key, *args, wait_time=wait_time)

    def _wait(self, expected_condition, json_key, wait_time=None):
        """
        :param expected_condition: selenium.webdriver.support.expected_condition object
        :param json_key: locator json key
        :param wait_time: time to wait
        :return: True if condition is reached within expected wait time. False otherwise

        """
        if wait_time is None:
            wait_time = self.wait_time

        wait = WebDriverWait(self.driver, wait_time)
        try:
            self.logger.debug(f"wait {wait_time} secs for {expected_condition}")
            self.driver.implicitly_wait(0)
            wait.until(expected_condition(self._get_locator(json_key)))
            condition = True
        except TimeoutException:
            condition = False
        finally:
            self.driver.implicitly_wait(self.wait_time)

        return condition

    def dynamic_wait(self, expected_condition, json_key, *args, wait_time=None):
        """
        :param expected_condition: selenium.webdriver.support.expected_condition object
        :param json_key: locator json key
        :param args: arguments to format json key
        :param wait_time: of time to wait
        :return: True if condition is reached within expected wait time. False otherwise

        """
        if wait_time is None:
            wait_time = self.wait_time

        wait = WebDriverWait(self.driver, wait_time)
        try:
            self.driver.implicitly_wait(0)
            wait.until(expected_condition(self._get_dynamic_locator(json_key, *args)))
            condition = True
        except TimeoutException:
            condition = False
        finally:
            self.driver.implicitly_wait(self.wait_time)

        return condition
    # endregion Wait

    # region Validation
    def _is_element_enabled(self, json_key):
        return self._get_element(json_key).is_enabled()

    def _is_dynamic_element_enabled(self, json_key, *args):
        return self._get_dynamic_element(json_key, *args).is_enabled()

    def _is_element_displayed(self, json_key):
        try:
            return self._get_element(json_key).is_displayed()
        except NoSuchElementException:
            return False

    def _is_dynamic_element_displayed(self, json_key, *args):
        try:
            return self._get_dynamic_element(json_key, *args).is_displayed()
        except NoSuchElementException:
            return False

    def _is_element_checked(self, json_key):
        return self._get_element(json_key).is_selected()

    def _is_dynamic_element_checked(self, json_key, *args):
        return self._get_dynamic_element(json_key, *args).is_selected()
    # endregion Validation

    # region Utilities
    def _execute_script(self, script, *args):
        self.logger.debug('script: %s' % script)
        response = self.driver.execute_script(script, *args)
        self.logger.debug('response: %s' % response)
        return response

    def _clear_element_data(self, json_key):
        by, locator = self._get_locator(json_key)
        self.driver.find_element(by, locator).clear()
    # endregion Utilities

    # region Browser Utilities
    def load_iframe(self, json_key='iframe'):
        self.driver.switch_to.frame(self._get_element(json_key))

    def back(self):
        self.driver.back()

    def switch_to_new_window(self):
        window_handles = self.driver.window_handles
        if len(window_handles) == 2:
            self.driver.switch_to.window(window_handles[1])
        elif len(window_handles) > 2:
            self.driver.switch_to.window(window_handles[len(window_handles) - 1])

    def switch_to_default_window(self):
        window_handles = self.driver.window_handles
        self.driver.switch_to.window(window_handles[0])

    def new_tab(self):
        self.driver.execute_script('''window.open("https://www.blank.org/","_blank");''')

    def refresh(self):
        self.driver.refresh()
    # endregion Browser Utilities

    # region Move / Scroll
    def _move_to_element(self, json_key):
        element = self._get_element(json_key)
        ActionChains(self.driver) \
            .move_to_element(element) \
            .perform()

    def _move_to_dynamic_element(self, json_key, *args):
        element = self._get_dynamic_element(json_key, *args)
        ActionChains(self.driver) \
            .move_to_element(element) \
            .perform()

    def _scroll_dynamic_element_into_view(self, json_key, *args):
        element = self._get_dynamic_element(json_key, *args)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def _scroll_element_into_view(self, json_key):
        element = self._get_dynamic_element(json_key)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)
    # endregion Move / Scroll

    # region Select
    def _select_option_by_text(self, key_pair, option):
        Select(self._get_element(key_pair)).select_by_visible_text(option)

    def _generic_selector(self, json_key, value, index=None):
        if index is None:
            self._click_element(json_key)
            self._wait_for_dynamic_element_clickable("generic_menu_item", value)
            self._click_dynamic_element("generic_menu_item", value)
            pass
        else:
            self._click_dynamic_element(json_key, index)
            self._click_dynamic_element("generic_menu_item", value, index)
    # endregion Select
