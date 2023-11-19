#!/usr/bin/python

import datetime
from appium import webdriver

from framework.utils.logger import Logger
from framework.utils.config_parser import ConfigParser


class TestObject(object):
    """
    Test Object that handles setup and teardown

    Helpful Reading:
        - https://www.selenium.dev/documentation/webdriver/
        - https://www.selenium.dev/documentation/webdriver/browsers/
        - https://www.selenium.dev/documentation/webdriver/waits/
        - https://www.selenium.dev/documentation/webdriver/drivers/
        - https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/

    """
    def setup_method(self):
        self.config = ConfigParser()

        self.logger = Logger().get_logger()

        # initialize webdriver
        self.init_webdriver()

        # webdriver session timestamp
        date = datetime.datetime.now()
        timestamp = date - datetime.timedelta(microseconds=date.microsecond)
        session_info = f'WebDriver session id - {str(self.webdriver.session_id)} - {timestamp}'

        # log start
        log = f'{"-"*80}\nSTART:\n{session_info}\n'
        self.logger.info(log)

    def init_webdriver(self):
        """
        Initialize webdriver instance and set desired capabilities
        """
        remote_command_executor_url = self.get_remote_executor_url()
        desired_capabilities = self.get_desired_capabilities()

        self.webdriver = webdriver.Remote(
            command_executor=remote_command_executor_url,
            desired_capabilities=desired_capabilities
        )

        self.additional_webdriver_configs()

    def get_remote_executor_url(self):
        return self.config['webDriver']['remoteCommandExecutorUrl']

    def get_desired_capabilities(self):
        configs = {}

        configs['browserName'] = self.config['webDriver']['browserName']
        configs['version'] = self.config['webDriver']['browserVersion']
        configs['chromeOptions'] = self.config['webDriver']['chromeOptions']
        configs['pageLoadStrategy'] = self.config['webDriver']['pageLoadStrategy']

        return configs

    def additional_webdriver_configs(self):
        self.max_wait_time = int(self.config['webDriver']['maximumWaitTime'])

        self.wait_time = int(self.config['webDriver']['webdriverImplicitWait'])
        self.webdriver.implicitly_wait(self.wait_time)

        width = self.config['webDriver']['screenResolution'].split('x')[0]
        height = self.config['webDriver']['screenResolution'].split('x')[1]
        self.webdriver.set_window_size(width, height)


    def teardown_method(self):
        # log end
        self.logger.debug('webdriver.quit')
        log = f'END\n{"-"*80}\n'
        self.logger.info(log)

        try:
            self.webdriver.quit()
        except Exception as e:
            self.logger.debug('Quit Error: ' + str(e))
