#!/usr/bin/env python

"""
Filename:       arlo-downloader.py
Description:    Check README.md or -h cli flag to see documentation about usage of the script.
Author:         Jeremy Diaz <jd@diaznet.ch>
Date:           2022-01-05
License:        MIT
"""

import logging
import os
import sys
import asyncio
from argparse import ArgumentParser, Namespace

import pyaarlo

from config import Config


def parse_arguments() -> Namespace:
    """
    This is a function that parses arguments given in the shell to the CLI.

    Returns:
        Namespace: A Namespace containing all arguments
    """

    parser = ArgumentParser(description='Download records from Arlo Cameras.')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable Debug messages. Can also be set with environment variable DEBUG=1')
    parser.add_argument('-m',
                        '--save-media-to',
                        help=f"Save Media naming scheme without extension (default = '{Config.config("save_media_to")}').",
                        action='store')
    parser.add_argument('-t',
                        '--tfa-type',
                        choices=['PUSH', 'EMAIL'],
                        help=f"Set TFA type (default = '{Config.config("tfa_type")}').",
                        action='store')
    parser.add_argument('-s',
                        '--tfa-source',
                        choices=['push', 'imap'],
                        help=f"Set TFA source (default = '{Config.config("tfa_source")}').",
                        action='store')
    parser.add_argument('-r',
                        '--tfa-retries',
                        help=f"Set TFA max retries (default = {Config.config("tfa_retries")}).",
                        type=int,
                        action='store')
    parser.add_argument('-D',
                        '--tfa-delay',
                        help=f"Set TFA delay between each check (default = {Config.config("tfa_delay")}).",
                        type=int,
                        action='store')
    parser.add_argument('-H',
                        '--tfa-host',
                        help=f"(EMAIL/imap only) Set TFA host (default = {Config.config("tfa_host")}).",
                        action='store')
    parser.add_argument('-U',
                        '--tfa-username',
                        help=f"(EMAIL/imap only) Set TFA username (default = {Config.config("tfa_username")}).",
                        action='store')
    parser.add_argument('-P',
                        '--tfa-password',
                        help=f"(EMAIL/imap only) Set TFA password (default = {Config.config("tfa_password")}).",
                        action='store')
    args = parser.parse_args()
    return args


def set_logger(dbg: bool) -> None:
    """
    Sets the logger to debug.

    Args:
        dbg (bool): Logger set to Debug if True
    """
    level = logging.INFO
    if dbg:
        level = logging.DEBUG
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%dT%H:%M:%S%z"
                        )


def init() -> None:
    """
    Initializes the connection to arlo and traps
    """
    # code to trap when attributes change
    def attribute_changed(device, attr, value):
        logging.info("attribute_changed: %s:%s:%s", device.name, attr, str(value)[:80])

    # set these from the environment to log in
    username = os.environ.get('ARLO_USERNAME', '_INVALID')
    password = os.environ.get('ARLO_PASSWORD', '_INVALID')

    # Print configuration in DEBUG
    for conf_item in Config.dump_config().items():
        logging.debug(conf_item)
    # log in
    # add `dump=True` to enable event stream packet dumps
    arlo = pyaarlo.PyArlo(username=username, password=password,
                          tfa_type=Config.config('tfa_type'),
                          tfa_source=Config.config('tfa_source'),
                          tfa_retries=Config.config('tfa_retries'),
                          tfa_delay=Config.config('tfa_delay'),
                          tfa_host=Config.config('tfa_host'),
                          tfa_username=Config.config('tfa_username'),
                          tfa_password=Config.config('tfa_password'),
                          synchronous_mode=False,
                          mode_api='v2',
                          save_state=True,
                          dump=False,
                          storage_dir='aarlo',
                          save_media_to=Config.config('save_media_to'))
    if not arlo.is_connected:
        logging.info("failed to login: %s", arlo._last_error)
        sys.exit(-1)

    # get base stations, list their statuses, register state change callbacks
    for base in arlo.base_stations:
        logging.info("base-name=%s, device_id=%s, state=%s", base.name, base.device_id, base.state)
        base.add_attr_callback('*', attribute_changed)

    # get cameras, list their statuses, register state change callbacks
    # * is any callback, you can use motionDetected just to get motion events
    for camera in arlo.cameras:
        logging.info("camera: name=%s,device_id=%s,state=%s", camera.name, camera.device_id, camera.state)
        camera.add_attr_callback('*', attribute_changed)


def main(args: Namespace):
    """
    Main entry point

    Args:
        args (Namespace): A Namespace containing all arguments
    """

    loop = asyncio.get_event_loop()
    if args.save_media_to:
        Config.set("save_media_to", args.save_media_to)
    if args.tfa_type:
        Config.set("tfa_type", args.tfa_type)
    if args.tfa_source:
        Config.set("tfa_source", args.tfa_source)
    if args.tfa_retries:
        Config.set("tfa_retries", args.tfa_retries)
    if args.tfa_delay:
        Config.set("tfa_delay", args.tfa_delay)
    if args.tfa_host:
        Config.set("tfa_host", args.tfa_host)
    if args.tfa_username:
        Config.set("tfa_username", args.tfa_username)
    if args.tfa_password:
        Config.set("tfa_password", args.tfa_password)
    if args.debug:
        set_logger(True)
    elif (os.environ.get('DEBUG') and os.environ.get('DEBUG') == '1'):
        set_logger(True)
    else:
        set_logger(False)
    try:
        init()
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        loop.close()


if __name__ == "__main__":

    arguments = parse_arguments()
    main(arguments)
