#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
files = "admin.db"
with open(files,"r") as f:
    data = json.load(f)
    print(data)