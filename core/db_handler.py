#!/usr/bin/env python
# -*- coding:utf8 -*-
import json,time,os,sys

from conf import settings
# from .conf import settings
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)


def db_handler():
    # connect to db
    conn_params = settings.DATABASE
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass


def file_db_handle(conn_params):
    # print('file db:',conn_params)
    return file_execute


def file_execute(sql,**kwargs):
    conn_params = settings.DATABASE
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])

    manager_conn_params = settings.MANAGER_DB
    manager_db_path = '%s/%s' % (manager_conn_params['path'], manager_conn_params['name'])

    # print(sql,db_path)
    sql_list = sql.split("where")
    # print(sql_list)
    if sql_list[0].startswith("select") and len(sql_list) > 1:
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            # print(account_file)
            if os.path.isfile(account_file):
                with open(account_file, "r") as f:
                    account_data = json.load(f)
                    return account_data
            else:
                exit("\033[31;1mAccount [%s] does not exist!\033[0m" % val)

        elif column == 'manager':
            manager_file = '%s/%s.db' % (manager_db_path, val)
            if os.path.isfile(manager_file):
                with open(manager_file, 'r') as f:
                    manager_data = json.load(f)
                    return manager_data
            else:
                exit("\033[31;1mAccount [%s] does not exist!\033[0m" % val)

    elif sql_list[0].startswith('update') and len(sql_list) > 1:
        column, val = sql_list[1].strip().split("=")
        if column == 'account':
            account_file = '%s/%s.json' % (db_path, val)
            if os.path.isfile(account_file):
                account_data = kwargs.get("account_data")
                with open(account_file,'w') as f:
                    acc_data = json.dump(account_data,f)
                return True


def goods_execute(sql, *args, **kwargs):
    conn_params = settings.GOODS_DB
    db_path = '%s/%s' % (conn_params['path'],conn_params['name'])

    sql_list = sql.split()
    if sql_list[0].startswith('select') and len(sql_list) > 1:
        val = sql_list[-1].strip()
        if val == 'goods.db':
            goods_file = '%s/%s' % (db_path,val)
            if os.path.isfile(goods_file):
                with open(goods_file, "r",encoding='utf-8') as f:
                    goods_data = json.load(f)
                    return goods_data

    elif sql_list[0].startswith('update') and len(sql_list) > 1:
        val = sql_list[-1].strip()
        if val == 'goods.db':
            goods_file = '%s/%s' % (db_path, val)
            if os.path.isfile(goods_file):
                goods_data = args[0]
                with open(goods_file,'w', encoding='utf-8') as f:
                    json.dump(goods_data, f, ensure_ascii=False, indent=4)
                return True






