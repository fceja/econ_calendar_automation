#!/usr/bin/python

import datetime

from appium import webdriver

from framework.utils.logger import Logger
from framework.utils.config_parser import ConfigParser


class TestObject(object):
    """
    This is a generic Test Object to handle setup and teardown

    """
    __test__ = False
    configuration = None
    logger = None

    webdriver = None
    webdriver_session_id = None
    device_data = None

    request = None
    test_name = None

    wait_time = None
    max_wait_time = None

    utils = None

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
        Initialize a driver instance and set the appropriate desired capabilities

        """
        # retreive webdriver re
        remote_command_executor_url = self.config['webDriver']['remoteCommandExecutorUrl']
        desired_capabilities = self.configure_desired_capabilities()

        self.webdriver = webdriver.Remote(
            command_executor=remote_command_executor_url,
            desired_capabilities=desired_capabilities
        )

        self.wait_time = int(self.config['webDriver']['webdriverImplicitWait'])
        self.max_wait_time = int(self.config['webDriver']['maximumWaitTime'])
        self.webdriver.implicitly_wait(self.wait_time)
        self.webdriver.set_window_size(self.config['webDriver']['screenResolution'].split(
            'x')[0], self.config['webDriver']['screenResolution'].split('x')[1])

    def configure_desired_capabilities(self):
        configs = {}

        configs['browserName'] = self.config['webDriver']['browserName']
        configs['version'] = self.config['webDriver']['browserVersion']
        configs['chromeOptions'] = self.config['webDriver']['chromeOptions']
        configs['sauce:options'] = self.config['webDriver']['options']
        configs['pageLoadStrategy'] = self.config['webDriver']['pageLoadStrategy']

        return configs

    def teardown_method(self):
        # log end
        self.logger.debug('webdriver.quit')
        log = f'END\n{"-"*80}\n'
        self.logger.info(log)

        try:
            self.webdriver.quit()
        except Exception as e:
            self.logger.debug('Quit Error: ' + str(e))
