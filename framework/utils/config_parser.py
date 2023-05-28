#!/usr/bin/python

"""
copyright: Copyright 2019, Value Stream Engineering
email: contact@valuestreamengineers.com
"""
import os
import json


class ConfigParser(object):
    """
    Handles the json configuration file that dictates
    test case scenarios. It's using an environment variable
    CONFIG_FILE to locate configuration file.

    """
    CONFIG_FILE_VARIABLE = 'CONFIG_FILE'

    def __init__(self, file_path=None):
        """
        File_path refers to the json document that contains test
        scenario details. By default it will use the value from
        CONFIG_FILE environment variable, but can be passed in
        as the first argument.

        :param file_path: If not supplied, uses environment variable CONFIG_FILE

        """
        if not file_path:
            file_path=os.getenv(self.CONFIG_FILE_VARIABLE)

        self.config_data = None
        self.validate_config_file(file_path)
        self.parse_config_file(file_path)

    def validate_config_file(self, file_path):
        """
        Validates the existence of the config file to be used
        for testing.

        """
        if not file_path:
            raise IOError("DEBUG --- Please set the '{0}' environment variable.".format(
                self.CONFIG_FILE_VARIABLE))

        if not os.path.exists(file_path):
            raise IOError("DEBUG --- Specified '{0}' did not exist.".format(file_path))

    def parse_config_file(self, file_path):
        with open(file_path, 'r+') as json_file:
            self.config_data = json.load(json_file)

    def __getitem__(self, key):
        try:
            return self.config_data[key]
        except:
            return None

