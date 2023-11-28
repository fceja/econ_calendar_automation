#!/usr/bin/python

import os
import json


class ConfigParser(object):
    """
    Parse config file properties.
    """
    CONFIG_DATA = None
    CONFIG_PATH_ENV_VAR = 'CONFIG_PATH'  # supplied in command-line

    def __init__(self, config_path=None):
        """
        :param config_path: use 'config_path' if provided, else use CONFIG_PATH_ENV_VAR'.
        """
        if not config_path:
            config_path = os.getenv(self.CONFIG_PATH_ENV_VAR)

        self.validate_config_path_exists(config_path)
        self.parse_config_file(config_path)

    def __getitem__(self, key):
        """
        Allows class instance to be treated like dictionary.

        Example:
        self.config = ConfigParser()
        self.config['getData']

        # if key exists on 'self.CONFIG_DATA', returns value, else None.
        """
        try:
            return self.CONFIG_DATA[key]
        except:
            return None

    def validate_config_path_exists(self, config_path):
        """
        Verifies config file path exists, else throws error.
        """
        if not config_path:
            raise IOError(
                f"'CONFIG_PATH' not provided in command-line pytest invocation.")

        if not os.path.exists(config_path):
            raise IOError(
                f"Provided 'CONFIG_PATH' does not exist -> [{config_path}]")

    def parse_config_file(self, config_path):
        with open(config_path, 'r+') as json_file:
            self.CONFIG_DATA = json.load(json_file)
