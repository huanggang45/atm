#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core import manager_main

if __name__ == '__main__':
    manager_main.run()
