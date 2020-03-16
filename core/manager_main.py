#!/usr/bin/env python
# -*- coding:utf8 -*-
from core import auth
from core import logger
from core import db_handler

access_logger = logger.logger("access")

user_data = {
    'is_authenticated': False,
    'account_data': None
}


def run():
    acc_data = auth.manager_acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)


def interactive(acc_data):
    menu = u'''
    ------ Manager Menu -------
    \033[32;1m1.添加购物(realize)
    2.用户额度(realize)
    3.冻结账户(realize)
    4.退出(realize)
    \033[0m'''

    menu_dic = {
        '1': update_goods,
        '2': user_credit,
        '3': blocked_account,
        '4': logout
    }

    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option](acc_data)
        else:
            print('\033[31;1mOption does not exist!\033[0m')


def update_goods(acc_data):
    menu_list = '''
        ------ 商品后台管理 -------
    \033[35;1m1.添加(realize)
    2.删除
    3.变更
    4.退出
    \033[0m
    '''
    # print(menu_list)
    goods = db_handler.goods_execute("select * from goods.db")
    print(goods)
    print("目前商品如下".center(20, '-'))

    for i in range(len(goods)):
        print(('''\033[32;1m%s. %s  %s\033[0m''') % (i, goods[i]['name'], goods[i]['price']))
    while True:
        goods_name = input("请输入要添加的商品名称(输入“q”退出)：").strip()
        if goods_name == "q":
            db_handler.goods_execute("update goods.db",goods)
            break
        goods_price = input("请输入该商品价格：").strip()
        if goods_price.isdigit():
            goods_price = int(goods_price)
        else:
            print("请输入正确的数字")
            continue
        add_goods = {"name": goods_name,"price":goods_price}
        goods.append(add_goods)


def user_credit(acc_data):
    account = input("pls input account id:").strip()
    if account.isdigit():
        db_api = db_handler.db_handler()
        account_data = db_api("select * from accounts where account=%s" % account)
        print("目前%s的额度是%s" % (account_data['id'], account_data['credit']))
        new_credit = input("pls input new credit:").strip()
        if new_credit.isdigit():
            account_data['credit'] = new_credit
            db_api("update accounts where account=%s" % account_data['id'], account_data=account_data)
    else:
        print("pls input correct num")


def blocked_account(acc_data):
    account = input("pls input account id:").strip()
    db_api = db_handler.db_handler()
    account_data = db_api("select * from accounts where account=%s" % account)
    blocked_status = input("是否冻结(y/n)").strip().lower()
    if blocked_status.isalpha():
        if blocked_status == 'y':
            account_data['status'] = 1
        elif blocked_status == 'n':
            account_data['status'] = 0

    db_api("update accounts where account=%s" % account_data['id'], account_data=account_data)


def logout(acc_data):
    print(acc_data)
    account_id = acc_data['account_data']['user']
    user_data['is_authenticated'] = False
    access_logger.info("account %s just log out Manage Page" % account_id)
    exit("user %s log out Manage Page..bye.." % account_id)
