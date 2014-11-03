#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import logging
from clique import runtime
from clique import web
import subprocess
from string import Template


def start():
  try:
    logging.info("Start...")
    web.set_static_path(os.path.join(runtime.res_dir(), 'web'))
    storage_path = os.path.join(runtime.home_dir(), '.sync')
    if not os.path.exists(storage_path):
      os.mkdir(storage_path)
    config_path = os.path.join(runtime.home_dir(), 'btsync.config')
    if not os.path.exists(config_path):
      config_template_path = os.path.join(runtime.res_dir(), 'btsync.config')
      with open(config_template_path, 'r') as f:
        config_str = f.read()
      logging.info("Creating a config file. %s", config_str)
      with open(config_path, 'w') as f:
        f.write(Template(config_str).substitute(device_name=runtime.app_name(),
                                                storage_path=storage_path))
    else:
      logging.debug("Using the existing config.")
    cmd = os.path.join(runtime.app_dir(), 'btsync')
    subprocess.check_call('{0} --config {1}'.format(cmd, config_path),
                          shell=True)
  except:
    logging.exception("Failed to start app.")
    raise


if __name__ == '__main__':
  start()
