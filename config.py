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
      "media_folder": os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "records",
      "filename": "${Y}/${m}/${F}T${t}_${N}_${SN}",
      "tfa_type": "PUSH",
      "tfa_source": "push",
      "tfa_retries": 10,
      "tfa_delay": 5,
      "tfa_host": '',
      "tfa_username": '',
      "tfa_password": ''
    }
    __setters = [
      "media_folder",
      "filename",
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
    def save_media_to() -> str:
        """
        Returns the full save_media_to path for pyaarlo (media_folder + filename).

        Returns:
            str: combined path
        """
        return Config.__conf["media_folder"] + "/" + Config.__conf["filename"]

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
        Sets a config value.

        Args:
            name (str): config key
            value: config value

        Raises:
            NameError: if name is not in allowed setters
        """

        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")
