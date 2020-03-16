#!/usr/bin/env python
# -*- coding:utf8
import os
from core import db_handler
import time


def login_required(func):
    # 验证用户是否登录

    def wrapper(*args,**kwargs):
        # print('----wrapper----',args,kwargs)
        # print((args[0]).get('is_authenticated'))
        if args[0].get('is_authenticated'):
            return func(*args,**kwargs)
        else:
            exit("User is not authenticated.")
    return wrapper


def acc_login(user_data, log_obj):
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 3:
        account = input("\033[32;1maccount:\033[0m").strip()
        password = input("\033[32;1mpassword:\033[0m").strip()
        auth_data = acc_auth2(account,password)
        if auth_data:
            user_data['is_authenticated'] = True
            user_data['account_id'] = account
            print(("Welcome %s".center(50,'-')) % account)
            log_obj.info("user %s just logged in " % user_data['account_id'])
            return auth_data
        retry_count += 1
    else:
        log_obj.error("account [%s] too many login attempts" % account)
        exit()


def acc_auth2(account, password):
    db_api = db_handler.db_handler()
    data = db_api("select * from accounts where account=%s" % account)

    if data['password'] == password:
        exp_time_stamp = time.mktime(time.strptime(data['expire_date'], "%Y-%m-%d"))
        if time.time() > exp_time_stamp:
            print('\033[31;1mAccount [%s] has expired,please contact the bank to get a new card! \033[0m'
                  % account)
        elif data['status'] == 1:
            print("\033[31;1mAccount [%s] has been blocked,pls contact the bank to unblocked!\033[0m" % account)

        else:
            return data
    else:
        print("\033[31;1mAccount ID or password is incorrect!\033[0m")


def manager_acc_login(user_data, log_obj):
    retry_count = 0
    while user_data['is_authenticated'] is not True and retry_count < 3:
        account = input("\033[32;1mManager user:\033[0m").strip()
        password = input("\033[32;1mPassword:\033[0m").strip()
        auth_data = manager_acc_auth(account,password)
        if auth_data:
            user_data['is_authenticated'] = True
            print(("Welcome %s".center(50,'-')) % account)
            log_obj.info("user %s just logged in " % auth_data['user'])
            return auth_data
        retry_count += 1
    else:
        log_obj.error("account [%s] too many login attempts" % account)
        exit()


def manager_acc_auth(account, password):
    db_api = db_handler.db_handler()
    data = db_api("select * from admin.db where manager=%s" % account)

    if data['password'] == password:
            return data
    else:
        print("\033[31;1mAccount ID or password is incorrect!\033[0m")

