#!/usr/bin/env python
#

import logging
import os
import sys
import time
import pprint
import pyaarlo
import asyncio 
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor Arlo Cameras.')
    parser.add_argument('-d',
                       '--debug',
                       action='store_true',
                       help='Enable Debug messages')
    parser.add_argument('-m',
                        '--save-media',
                        help='Save Media naming scheme',
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

def Init(media_location):

    # code to trap when attributes change
    def attribute_changed(device, attr, value):
        logging.info('attribute_changed:' + device.name + ':' + attr + ':' + str(value)[:80])

    # set these from the environment to log in
    USERNAME = os.environ.get('ARLO_USERNAME', '_INVALID')
    PASSWORD = os.environ.get('ARLO_PASSWORD', '_INVALID')
    # log in
    # add `verbose_debug=True` to enable even more debugging
    # add `dump=True` to enable event stream packet dumps
    arlo = pyaarlo.PyArlo(username=USERNAME, password=PASSWORD,
                        tfa_type='SMS', tfa_source='console', synchronous_mode=True,
                        save_state=False, dump=False, storage_dir='aarlo', verbose_debug=True, save_media_to=media_location)
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
    script_path = os.path.dirname(os.path.realpath(__file__))
    filename_pattern = '${Y}/${m}/${F}T${t}_${N}_${SN}.mp4'
    
    save_media_to = script_path + filename_pattern
    
    #set_logger(False)
    
    loop = asyncio.get_event_loop()
    if arguments.save_media:
        save_media_to = arguments.save_media
    if arguments.debug:
        set_logger(True)
    else:
        set_logger(False)
    try:
        Init(save_media_to)
        loop.run_forever()
    finally:
        loop.close()

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments)