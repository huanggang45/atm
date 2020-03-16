#!/usr/bin/env python
# -*- coding:utf8 -*-
# handle all the logger works

import logging
from conf import settings


def logger(log_type):

    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # creat console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = '%s/log/%s' %(settings.BASE_DIR,settings.LOG_TYPE[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to loggger
    # logger.addHandler(ch)
    logger.addHandler(fh)

    return logger