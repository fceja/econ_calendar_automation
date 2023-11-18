import logging
import logging.handlers

import os
from pathlib import Path

from framework.utils.config_parser import ConfigParser

loggers = {}


class Logger(object):
    """
    """

    __file_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0])

    def __init__(self, application_name, *args, **kwargs):
        self.config = ConfigParser()
        self.app = application_name

    def get_logger(self, name):
        if loggers.get(name):
            return loggers.get(name)
        else:
            logger = logging.getLogger(name)
            logger.setLevel(self.config['logLevel'].upper())

            log_dir = os.path.join(self.__file_dir, '..', '..', 'logs')
            Path(log_dir).mkdir(parents=True, exist_ok=True)

            log_filename = os.path.join(log_dir, name + '.log')
            handler = logging.handlers.RotatingFileHandler(
                log_filename,
                maxBytes=(1024*1024)*500,  # 500 M #TODO: Define in config?
                backupCount=1
            )

            formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            loggers[name] = logger

            return logger
