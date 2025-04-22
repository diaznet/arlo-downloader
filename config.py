#!/usr/bin/env python

"""
Filename:       config.py
Description:    configuration class for arlo-downloader.py.
Author:         Jeremy Diaz <jd@diaznet.ch>
Date:           2022-01-05
License:        MIT
"""

import os


class Config:
    """
    Config class is handling configuration
    """

    __conf = {
      "save_media_to": os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "${Y}" + os.path.sep + "${m}" + os.path.sep + "${F}T${t}_${N}_${SN}",
      "tfa_type": "PUSH",
      "tfa_source": "push",
      "tfa_retries": 10,
      "tfa_delay": 5,
      "tfa_host": '',
      "tfa_username": '',
      "tfa_password": ''
    }
    __setters = [
      "set_logger",
      "save_media_to",
      "tfa_type",
      "tfa_source",
      "tfa_retries",
      "tfa_delay",
      "tfa_host",
      "tfa_username",
      "tfa_password"
      ]

    @staticmethod
    def config(name: str) -> str:
        """
        Returns a key value in the config

        Args:
            name (str): Name of the key

        Returns:
            dict: key's value
        """

        return Config.__conf[name]

    @staticmethod
    def dump_config() -> dict:
        """
        Dumps the whole config

        Returns:
            dict: dictionnary representing the config
        """

        return Config.__conf

    @staticmethod
    def set(name, value):
        """
        _summary_

        Args:
            name (_type_): _description_
            value (_type_): _description_

        Raises:
            NameError: _description_
        """

        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")
