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

    driver = None
    session_id = None
    device_data = None

    request = None
    test_name = None

    wait_time = None
    max_wait_time = None

    utils = None

    def setup_method(self):
        self.config = ConfigParser()

        self.logger = Logger().get_logger()

        # Controller setup
        self.init_driver()

        # Session info
        self.session_id = self.driver.session_id

        # Session Timestamp
        date = datetime.datetime.now()
        timestamp = date - datetime.timedelta(microseconds=date.microsecond)

        session_info = '\nSESSION_ID[{0}]: {1}'.format(timestamp, str(self.session_id))

        # Log Start
        log = '\n' + \
              '-'*80 + '\n' + \
              'START TEST:\n' + \
              '-'*80 + '\n' + session_info + '\n'
        self.logger.info(log)

        # self.utils = Utils()

    def init_driver(self):
        """
        Initialize a driver instance and set the appropriate desired capabilities

        """
        # retreive webdriver re
        remote_command_executor_url = self.config['webDriver']['remoteCommandExecutorUrl']
        desired_capabilities = self.configure_desired_capabilities()

        self.driver = webdriver.Remote(
            command_executor=remote_command_executor_url,
            desired_capabilities=desired_capabilities
        )

        self.wait_time = int(self.config['webDriver']['webdriverImplicitWait'])
        self.max_wait_time = int(self.config['webDriver']['maximumWaitTime'])
        self.driver.implicitly_wait(self.wait_time)
        self.driver.set_window_size(self.config['webDriver']['screenResolution'].split(
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
        self.logger.debug('driver.quit')
        # Log Exit
        log = '\n' + \
              '-' * 80 + '\n' + \
              'END TEST: ' + '\n' + \
              '-' * 80 + '\n'
        self.logger.info(log)
        try:
            self.driver.quit()
        except Exception as e:
            self.logger.debug('Quit Error: ' + str(e))
