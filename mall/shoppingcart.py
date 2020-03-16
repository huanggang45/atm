#!/usr/bin/env python
# -*- coding:utf8 -*-
# import os
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)
import time
from core import db_handler
from core import transaction


def shopping(account_data, trans_logger):
    goods = db_handler.goods_execute("select * from goods.db")
    print("商品列表".center(20, '-'))
    for i in range(len(goods)):
        print(('''\033[32;1m%s. %s  %s\033[0m''') % (i, goods[i]['name'], goods[i]['price']))

    shopping_cart = []
    while True:
        choice = input("请选择商品序号：(input 'q' to exit)").strip()
        if choice.isdigit():
            choice = int(choice)
            if choice >=0 and choice < len(goods):
                if account_data['balance'] >= float(goods[choice]['price']):
                    shopping_cart.append(goods[choice])
                    print(goods[choice]['name'], "现已加入购物车")
                else:
                    print("\033[31;1m现金不足，请充值\033[0m")
                    continue
            else:
                print("\033[31;1m你输入的商品不存在\033[0m")

        elif choice == 'q':
            money = 0
            for t in shopping_cart:
                money += t['price']
            if money < account_data['balance'] and len(shopping_cart) > 0:
                print("======================")
                print("\033[34;1m当前ATM还剩下: %s\033[0m" % (account_data['balance']-money))
                print("你已经购买以下商品".center(20, "-"))
                for index, p in enumerate(shopping_cart):
                    print("\033[35;1m%s.%s  %s\033[0m" % (index, shopping_cart[index]['name'],
                                                          shopping_cart[index]['price']))
                time.sleep(3)
                transaction.make_transaction(trans_logger, account_data, 'consume', money)
                break
            else:
                print("\033[31;1m账户余额不足，请重新选购商品\033[0m")
                shopping_cart.clear()
                continue
