#!/srv/robotice/bin/python

import sys
import logging

from oslo.config import cfg
from oslo.config import types

import sensor

logging.basicConfig(level=logging.DEBUG)

common_opts = [
    cfg.Opt('name',
            short='n',
            default="cc2541",
            help='Sensor name'),
    cfg.Opt('mac',
            short='m',
            help='MAC address'),
]

CONF = cfg.CONF
CONF.register_cli_opts(common_opts)
CONF(sys.argv[1:])

print(sensor.get_data(CONF))
