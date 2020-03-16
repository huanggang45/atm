#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
file = 'transactions.log'
with open(file,"r",) as f:
    data = f.readlines()
    temp = []
    for line in data:
        if "1234" in line:
            temp.append(line)

    for v in temp:
        # print(v.split("-"))
        dic={}
        show_data = v.split("-")
        Year,Month,Time,Tran,Level,Other= show_data
        Time1,Time2 = Time.split(',')
        print(Other.split())
        # print(("%s-%s-%s") %(Year,Month,Time1))
"""