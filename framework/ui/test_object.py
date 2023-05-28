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
        self.logger = Logger(application_name='framework').get_logger(name='application')
        self.configuration = ConfigParser()

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
        remote_server_url = self.configuration['remoteServerUrl']

        desired_capabilities = self.configure_desired_capabilities()

        self.driver = webdriver.Remote(
            command_executor=remote_server_url,
            desired_capabilities=desired_capabilities
        )

        self.wait_time = int(self.configuration['webdriverImplicitWait'])
        self.max_wait_time = int(self.configuration['maximumWaitTime'])
        self.driver.implicitly_wait(self.wait_time)
        self.driver.set_window_size(self.configuration['screenResolution'].split('x')[0], self.configuration['screenResolution'].split('x')[1])


    def configure_desired_capabilities(self):
        configurations = {}

        configurations['automationName'] = self.configuration['automationName']
        configurations['browserName'] = self.configuration['browserName']
        configurations['version'] = self.configuration['browserVersion']
        configurations['platform'] = self.configuration['platformName']
        configurations['name'] = self.configuration['testName']
        configurations['sauce:options'] = self.configuration['options']
        configurations['pageLoadStrategy'] = self.configuration['pageLoadStrategy']
        configurations['chromeOptions'] = self.configuration['chromeOptions']

        return configurations

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
