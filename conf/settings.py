#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': '%s/db' % BASE_DIR
}

MANAGER_DB = {
    'engine': 'file_storage',
    'name': 'manager',
    'path': '%s/db' % BASE_DIR
}


GOODS_DB = {
    'engine': 'file_storage',
    'name': 'goods',
    'path': '%s/db' % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPE = {
    'transaction': 'transactions.log',
    'access': 'access.log'
}

TRANSACTION_TYPE = {
    'repay': {'action': 'plus', 'interest': 0},
    'collection': {'action': 'plus', 'interest': 0},
    'withdraw': {'action': 'minus', 'interest': 0.05},
    'transfer': {'action': 'minus', 'interest': 0.05},
    'consume': {'action': 'minus', 'interest': 0}
}

