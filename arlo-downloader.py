#!/usr/bin/env python

import logging
import os
import sys
import pyaarlo
import asyncio 
import argparse

from config import Config

def parse_arguments():
    
    parser = argparse.ArgumentParser(description='Download records from Arlo Cameras.')
    parser.add_argument('-d',
                       '--debug',
                       action='store_true',
                       help='Enable Debug messages')
    parser.add_argument('-m',
                        '--save-media-to',
                        help="Save Media naming scheme (default = \'{}\')".format(Config.config("save_media_to")),
                        action='store')
    parser.add_argument('-t',
                        '--tfa-type',
                        choices=['PUSH', 'EMAIL'],
                        help="Set TFA type (default = \'{}\')".format(Config.config("tfa_type")),
                        action='store')
    parser.add_argument('-s',
                        '--tfa-source',
                        choices=['push', 'imap'],
                        help="Set TFA source (default = \'{}\')".format(Config.config("tfa_source")),
                        action='store')
    parser.add_argument('-r',
                        '--tfa-retries',
                        help="Set TFA max retries (default = {}).".format(Config.config("tfa_retries")),
                        type=int,
                        action='store')
    parser.add_argument('-D',
                        '--tfa-delay',
                        help="Set TFA delay between each check (default = {}).".format(Config.config("tfa_delay")),
                        type=int,
                        action='store')
    parser.add_argument('-H',
                        '--tfa-host',
                        help="(EMAIL/imap only) Set TFA host (default = {}).".format(Config.config("tfa_host")),
                        action='store')
    parser.add_argument('-U',
                        '--tfa-username',
                        help="(EMAIL/imap only) Set TFA username (default = {}).".format(Config.config("tfa_username")),
                        action='store')
    parser.add_argument('-P',
                        '--tfa-password',
                        help="(EMAIL/imap only) Set TFA password (default = {}).".format(Config.config("tfa_password")),
                        action='store')
    args = parser.parse_args()
    return args

def set_logger(dbg):
    level = logging.INFO
    if (dbg):
        level = logging.DEBUG
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt="%Y-%m-%dT%H:%M:%S%z"
                        )
    _LOGGER = logging.getLogger(__file__) 

def Init():

    # code to trap when attributes change
    def attribute_changed(device, attr, value):
        logging.info('attribute_changed:' + device.name + ':' + attr + ':' + str(value)[:80])

    # set these from the environment to log in
    USERNAME = os.environ.get('ARLO_USERNAME', '_INVALID')
    PASSWORD = os.environ.get('ARLO_PASSWORD', '_INVALID')
    print(Config.config('tfa_delay'))
    # log in
    # add `verbose_debug=True` to enable even more debugging
    # add `dump=True` to enable event stream packet dumps
    arlo = pyaarlo.PyArlo(username=USERNAME, password=PASSWORD,
                        tfa_type=Config.config('tfa_type'),
                        tfa_source=Config.config('tfa_source'),
                        tfa_retries=Config.config('tfa_retries'),
                        tfa_delay=Config.config('tfa_delay'),
                        tfa_host=Config.config('tfa_host'),
                        tfa_username=Config.config('tfa_username'),
                        tfa_password=Config.config('tfa_password'),
                        synchronous_mode=True,
                        save_state=False,
                        dump=False,
                        storage_dir='aarlo',
                        verbose_debug=True,
                        save_media_to=Config.config('save_media_to'))
    if not arlo.is_connected:
        logging.info("failed to login({})".format(arlo._last_error))
        sys.exit(-1)

    # get base stations, list their statuses, register state change callbacks
    for base in arlo.base_stations:
        logging.info("base: name={},device_id={},state={}".format(base.name,base.device_id,base.state))
        base.add_attr_callback('*', attribute_changed)

    # get cameras, list their statuses, register state change callbacks
    # * is any callback, you can use motionDetected just to get motion events
    for camera in arlo.cameras:
        logging.info("camera: name={},device_id={},state={}".format(camera.name,camera.device_id,camera.state))
        camera.add_attr_callback('*', attribute_changed)

def main(arguments):
     
    loop = asyncio.get_event_loop()
    if arguments.save_media_to:
        Config.set("save_media_to", arguments.save_media_to)
    if arguments.tfa_type:
        Config.set("tfa_type", arguments.tfa_type)
    if arguments.tfa_source:
        Config.set("tfa_source", arguments.tfa_source)
    if arguments.tfa_retries:
        Config.set("tfa_retries", arguments.tfa_retries)
    if arguments.tfa_delay:
        Config.set("tfa_delay", arguments.tfa_delay)
    if arguments.tfa_host:
        Config.set("tfa_host", arguments.tfa_host)
    if arguments.tfa_username:
        Config.set("tfa_username", arguments.tfa_username)
    if arguments.tfa_password:
        Config.set("tfa_password", arguments.tfa_password)
    if arguments.debug:
        set_logger(True)
    else:
        set_logger(False)
    try:
        Init()
        loop.run_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        loop.close()

if __name__ == "__main__":

    arguments = parse_arguments()
    main(arguments)
 