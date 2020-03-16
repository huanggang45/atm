#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import importlib

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# from core import main
main = importlib.import_module('core.main')

if __name__ == '__main__':
    main.run()
