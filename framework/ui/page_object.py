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
    The base class for all mobile automation page objects

    """
    locator_json = None
    driver = None
    wait_time = None
    max_wait_time = None

    config = None

    width = None
    height = None

    utils = None

    def __init__(self, driver):
        """
        This provide access to the property file for the page and the
            controller instance to be used to access the page


        :param driver: Webdriver instance

        """
        self.logger = Logger(application_name='framework').get_logger(name='application')

        self.load_json_locator_file()
        self.configuration = ConfigParser()

        # Controller setup
        self.driver = driver

        screen_size = self.driver.get_window_size()
        self.width = screen_size['width']
        self.height = screen_size['height']

        self.wait_time = int(self.config['webDriver']['webdriverImplicitWait'])
        self.max_wait_time = int(self.config['webDriver']['maximumWaitTime'])

        # self.utils = Utils()

    def load_json_locator_file(self):
        """
        This method will try and load a default locator file based on the
        class that initialized it. This will work if the name of the class
        and the locator file are the same.
        Example:
            - class name: start.py
            - locator file: start.json
        """
        json_locator_file_path = os.path.abspath(inspect.getfile(self.__class__)).replace('.py', '.json')
        self.logger.debug(json_locator_file_path)
        if os.path.isfile(json_locator_file_path):
            with open(json_locator_file_path) as json_file:
                self.locator_json = json.load(json_file)

    @staticmethod
    def _pause(wait=0):
        """
        Sleeps for a given about of time

        :param wait: How long to wait in seconds
        :return: None

        """
        time.sleep(wait)

    # region Focus
    def __has_focus(self, element):
        """
        try to determine the elements focus state

        """
        focused = None
        selected = None

        try:
            focused = element.get_attribute('focused') == 'true'
        except:
            # No such attribute
            pass

        try:
            selected = element.get_attribute('selected') == 'true'
        except:
            # No such attribute
            pass

        return selected or focused

    # endregion

    # region Clickers
    def _double_click_element(self, json_key):
        """
        Web element click action that requires a locator key

        :param json_key: Json Key
        :return: None

        """
        self.logger.debug("_double_click_element")
        element = self._get_element(json_key)
        ActionChains(self.driver) \
            .double_click(element) \
            .perform()

    def _click_element(self, json_key):
        """
        Web element click action that requires a locator key

        :param json_key: Json Key
        :return: None

        """
        self.logger.debug("_click_element")
        element = self._get_element(json_key)
        try:
            element.click()
        except:
            element.click()

    def _click_dynamic_element(self, json_key, *args):
        """
        Web element click action using 'args' to format locator values

        :param json_key: Locator key
        :param args: Arguments used to dynamically format the locator
        :return: None

        """
        self.logger.debug("_click_dynamic_element")
        element = self._get_dynamic_element(json_key, *args)

        element.click()

    def _action_click_element(self, json_key):
        """
        ActionChains click that requires a locator key

        :param json_key: Locator key
        :return: None

        """
        self.logger.debug("_action_click_element")
        element = self._get_element(json_key)

        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def _action_dynamic_click_element(self, json_key, *args):
        """
        ActionChains click  using 'args' to format locator values

        :param json_key: Locator key
        :return: None

        """
        self.logger.debug("_action_dynamic_click_element")
        element = self._get_dynamic_element(json_key, *args)

        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def _option_click_element(self, json_key, wait_time=0):
        """
        Click method for elements with finicky elements

        :param json_key: Locator key
        :param wait_time: Wait time
        :return: None

        """
        self.logger.debug("_option_click_element")
        time.sleep(wait_time)

        key_pair_value = self.locator_json[json_key]
        by_value = key_pair_value['by']
        locator_value = key_pair_value['locator']
        element = self.driver.find_element(by_value, locator_value)

        try:
            element.click()
        # except:
        #     if self._is_element_displayed(json_key):
        #         ActionChains(self.driver) \
        #             .move_to_element(element) \
        #             .click(element) \
        #             .perform()
        finally:
            if self._is_element_displayed(json_key):
                ActionChains(self.driver) \
                    .move_to_element(element) \
                    .click(element) \
                    .perform()

    # endregion

    # region Getters
    def _get_dynamic_element(self, json_key, *args):
        """
        Use the dynamic xpath locator to find a web_element without changing the original json value

        :param json_key: Json locator key
        :param args: Arguments used to dynamically format the locator
        :return: web_element

        """
        self.logger.debug("_get_dynamic_element")
        by, locator = self._get_dynamic_locator(json_key, *args)
        return self.driver.find_element(by, locator)

    def _get_element(self, json_key):
        """
        Given a json, return a web_element

        :param json_key: Json locator key
        :return: web_element
        """
        self.logger.debug("_get_element")
        by, locator = self._get_locator(json_key)
        return self.driver.find_element(by, locator)

    def _get_locator(self, json_key):
        """
        Get the locator as a 'By' search type

        :param json_key: Json locator key
        :return: By locator tuple

        """
        self._pause()

        key_pair_value = self.locator_json[json_key]

        by_value = key_pair_value['by']
        locator_value = key_pair_value['locator']
        self.logger.debug("by: {by} locator: {locator}".format(
            by=by_value, locator=locator_value)
        )
        return by_value, locator_value

    def _get_dynamic_locator(self, json_key, *args):
        """
        Get the locator as a 'By' search type

        :param json_key: Json locator key
        :param args: Arguments used to dynamically format the locator
        :return: By locator tuple

        """
        self._pause()

        key_pair_value = self.locator_json[json_key]

        by_value = key_pair_value['by']
        locator_value = key_pair_value['locator'].format(*args)
        self.logger.debug("by: {by} locator: {locator}".format(
            by=by_value, locator=locator_value)
        )
        return by_value, locator_value

    def _get_element_text(self, json_key):
        """
        Get the text property of the web element

        :param json_key: Json locator key
        :return: a string value

        """
        element = self._get_element(json_key)
        text = element.text.strip()

        self.logger.debug('text: "%s"' % text)
        return text

    def _get_elements_text(self, json_key):
        """
        Get the text property of a list of web elements

        :param json_key: Json locator key
        :return: a list of string

        """
        strings = []
        elements = self._get_elements(json_key)
        for element in elements:
            strings.append(element.text.strip())

        self.logger.debug(strings)
        return strings

    def _get_dynamic_elements_text(self, json_key, *args):
        """
        Get the text property of a list of web elements using a dynamic locator

        :param json_key: Json locator key
        :param args: Arguments used to dynamically format the locator
        :return: a list of string

        """
        strings = []
        elements = self._get_dynamic_elements(json_key, *args)
        for element in elements:
            strings.append(element.text.strip())
        self.logger.debug('strings: ' + str(strings))
        return strings

    def _get_dynamic_element_text(self, json_key, *args):
        """
        Get the text property of the web element

        :param json_key: Json locator key
        :param args: Arguments used to dynamically format the locator
        :return: a string value

        """
        element = self._get_dynamic_element(json_key, *args)
        text = element.text.strip()
        self.logger.debug('text: ' + str(text))
        return text

    def _get_elements(self, json_key):
        """
        Given a json_key, returns a collection of web_elements

        :param json_key: Json locator key
        :return: web_elements list
        """
        self.logger.debug("_get_elements")
        by, locator = self._get_locator(json_key)
        return self.driver.find_elements(by, locator)

    def _get_dynamic_elements(self, json_key, *args):
        """
        Given a json_key, returns a collection of web_elements

        :param json_key: Json locator key
        :param args: Arguments used to dynamically format the locator
        :return: web_elements list
        """
        self.logger.debug("_get_dynamic_elements")
        by, locator = self._get_dynamic_locator(json_key, *args)
        return self.driver.find_elements(by, locator)

    def _get_elements_attribute(self, json_key, attr):
        """
        Get the attribute property of a list of web element

        :param json_key: Json locator key
        :param attr: attribute key
        :return: a list of string

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
        Get the attribute property of a list of web element

        :param json_key: Json locator key
        :param attr: attribute key
        :param args: Arguments used to dynamically format the locator
        :return: a list of string

        """
        elements = self._get_dynamic_elements(json_key, *args)
        attributes = []
        for e in elements:
            value = e.get_attribute(attr)
            if value:
                value = value.strip()
            attributes.append(value)

        return attributes

    def _get_elements_css_property(self, json_key, prop):
        """
        Get the css property value of a list of web element

        :param json_key: Json locator key
        :param prop: property key
        :return: a list of string

        """
        elements = self._get_elements(json_key)
        css_values = []
        for e in elements:
            value = e.value_of_css_property(prop)
            if value:
                value = value.strip()
            css_values.append(value)

        return css_values

    def _get_element_css_property(self, json_key, prop):
        """
        Get the css property value of the web element

        :param json_key: Json locator key
        :param prop: property key
        :return: a list of string

        """
        value = self._get_element(json_key).value_of_css_property(prop)
        if value:
            value = value.strip()
        return value

    def _get_element_attribute(self, json_key, attr):
        """
        Get the attribute property of the web element

        :param json_key: Json locator key
        :param attr: attribute key
        :return: a list of string

        """
        self.logger.debug("_get_element_attribute " + str(attr))
        value = self._get_element(json_key).get_attribute(attr)
        if value:
            value = value.strip()
        self.logger.debug(str(value))
        return value

    def _get_dynamic_element_attribute(self, json_key, attr, *args):
        """
        Get the attribute property of the web element

        :param json_key: Json locator key
        :param attr: attribute key
        :param *args: arguments
        :return: a list of string

        """
        self.logger.debug("_get_dynamic_element_attribute " + str(attr))
        value = self._get_dynamic_element(json_key, *args).get_attribute(attr)
        if value:
            value = value.strip()
        self.logger.debug(str(value))
        return value

    def _get_checkbox_state(self, json_key):
        """
        Get the state of the checkbox web element

        :param json_key: Json locator key
        :return: boolean True or False

        """
        self.logger.debug("_get_element_attribute " + "checked")
        value = self._get_element(json_key).get_attribute("checked")
        if value == "true":
            return True
        else:
            return False

    def _get_table(self, table_headers_json_key, table_rows_json_key, table_data_json_key):
        """
        Gets a list of dictionaries representing the table

        :param table_headers_json_key: Json locator key for table headers
        :param table_rows_json_key: Json locator key for table rows
        :param table_data_json_key: Json locator key for table data

        :return: [{'': ''}]
        """
        table = []

        table_rows = self._get_elements(table_rows_json_key)
        table_headers = self._get_table_headers(table_headers_json_key)

        for row in range(len(table_rows)):
            row += 1  # None zero index

            table_data = self._get_dynamic_elements(table_data_json_key, str(row))
            table.append((self._get_row_values(table_headers, table_data)))

        return table

    def _get_table_headers(self, table_headers_json_key):
        """
        Gets the table Header text and returns it in a List

        :param table_headers_json_key: Json locator key for table headers
        :return:  ['']
        """
        table_headers = self._get_elements(table_headers_json_key)
        header_text = []

        for header in table_headers:
            value = header.text.strip().split('\n')[0]
            header_text.append(value)

        header_text = list(filter(None, header_text))
        return header_text

    def _get_row_values(self, table_headers, table_data):
        """
        Gets table headers and table date rows and combines the { key-pair : value }

        :param table_headers: array of table headers
        :param table_data: list of table data
        :return:  [{'': ''}]
        """
        new_table_data = []
        for value in table_data:
            value = value.text.strip()
            new_table_data.append(value)

        new_table_data = list(filter(None, new_table_data))

        i = 0
        row = {}
        for data in new_table_data:
            row[table_headers[i]] = data
            i += 1
        return row

    def _get_table_row(self, index):
        """
        Returns a single row from the table as a dictionary^M

        :param index:
        :return: {'': ''}
        """
        row_data = self._get_dynamic_elements('table_data', str(index))
        return self._get_row_values(self._get_table_headers('table_headers'), row_data)

    def _get_stateroom_row(self, index):
        """
        Returns a single row from the stateroom table as a dictionary

        :param index:
        :return: {'': ''}
        """
        row_data = self._get_dynamic_elements('stateroom_cat_data', str(index))
        return self._get_row_values(self._get_table_headers('stateroom_cat_headers'), row_data)

    # endregion

    # region Setters
    def __send_keys(self, element, value):
        self.logger.debug("__send_keys " + str(value))
        element.send_keys(str(value))

    def _set_element_value(self, json_key, value):
        """
        Set value for input

        :param json_key: Json locator key
        :param value: The string value to set
        :return: None

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
        Set value for input

        :param json_key: Json locator key
        :param value: The string value to set
        :return: None

        """
        element = self._get_dynamic_element(json_key, *args)
        self.__send_keys(element, value)

    # endregion

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

    def _wait_for_element_stale(self, element, wait_time=None):
        if wait_time is None:
            wait_time = self.wait_time

        wait = WebDriverWait(self.driver, wait_time)
        try:
            self.logger.debug("wait {wait_time} secs for {expected_condition}".format(
                wait_time=wait_time, expected_condition='staleness_of'
            ))
            self.driver.implicitly_wait(0)
            wait.until(EC.staleness_of(element))
            condition = True
        except TimeoutException:
            condition = False
        finally:
            self.driver.implicitly_wait(self.wait_time)

        return condition

    def _wait(self, expected_condition, json_key, wait_time=None):
        """
        :param expected_condition: selenium.webdriver.support.expected_condition object
        :param json_key: The json locator key
        :param wait_time: The amount of time to wait, default is WebdriverImplicitWait in json config
        :return: True if condition is reached within expected wait time. False otherwise

        """
        if wait_time is None:
            wait_time = self.wait_time

        wait = WebDriverWait(self.driver, wait_time)
        try:
            self.logger.debug("wait {wait_time} secs for {expected_condition}".format(
                wait_time=wait_time, expected_condition=expected_condition.__name__
            ))
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
        :param json_key: The json locator key
        :param args: Arguments used to dynamically format the locator
        :param wait_time: The amount of time to wait, default is WebdriverImplicitWait in json config
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

    # endregion

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

    # endregion

    # region Utilities
    def _execute_script(self, script, *args):
        self.logger.debug('script: %s' % script)
        response = self.driver.execute_script(script, *args)
        self.logger.debug('response: %s' % response)
        return response

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

    def _clear_element_data(self, json_key):
        by, locator = self._get_locator(json_key)
        self.driver.find_element(by, locator).clear()

    def load(self, json_key='iframe'):
        self._pause(5)
        self.driver.switch_to.frame(self._get_element(json_key))

    def exit(self):
        self.driver.switch_to.default_content()

    def back(self):
        self.driver.back()

    def scroll_dynamic_element_into_view(self, json_key, *args):
        element = self._get_dynamic_element(json_key, *args)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def scroll_element_into_view(self, json_key):
        element = self._get_dynamic_element(json_key)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

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
    # endregion

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
