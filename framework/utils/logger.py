#!/usr/bin/python

import logging
import logging.handlers
import os
from pathlib import Path

from framework.utils.config_parser import ConfigParser


loggers = {}
class Logger(object):
    """
    Initiate logger Instance
    """

    def __init__(self):
        self.config = ConfigParser()

    def get_logger(self):
        # check if logs already exist, else create
        log_name = self.config['logger']['logName'];
        if loggers.get(log_name):
            return loggers.get(log_name)
        else:
            __file_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0])

            logger = logging.getLogger(log_name)
            logger.setLevel(self.config['logger']['logLevel'].upper())

            log_dir = os.path.join(__file_dir, '..', '..', 'logs')
            Path(log_dir).mkdir(parents=True, exist_ok=True)

            log_filename = os.path.join(log_dir, log_name + '.log')
            handler = logging.handlers.RotatingFileHandler(
                log_filename,
                maxBytes=(1024*1024)*1000,
            )

            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s')
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            loggers[log_name] = logger

            return logger
