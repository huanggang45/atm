#!/usr/bin/env python
# -*- coding:utf8 -*-
from core import auth
from core import accounts
from core import logger
from core import transaction
from core.auth import login_required
from mall import shoppingcart

trans_logger = logger.logger('transaction')
access_logger = logger.logger('access')

user_data = {
    'account_id': None,
    'is_authenticated': False,
    'account_data': None
}

@login_required
def account_info(acc_data):
    exit_flag = False
    print(("%s INFO").center(50, '-') % (acc_data['account_data']['id']))
    for k,v in acc_data['account_data'].items():
        if k not in ('password'):
            print("%25s: %s" % (k, v))
    print("END".center(50, '-'))

    while not exit_flag:
        exit_button = input("\033[33;1mInput 'b' return to menu:\033[0m").strip()
        if exit_button == 'b':
            exit_flag = True


def run():
    acc_data = auth.acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        interactive(user_data)


def interactive(acc_data):
    menu = u'''
    ------ Oldboy Bank -------
    \033[32;1m1.账户信息(realize)
    2.还款(realize)
    3.取款(realize)
    4.转账(realize)
    5.账单
    6.购物商城(realize)
    7.退出(realize)
    \033[0m'''

    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,
        '5': pay_check,
        '6': shopping_cart,
        '7': logout,
    }

    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            # print('accdata',acc_data)
            menu_dic[user_option](acc_data)
        else:
            print('\033[31;1mOption does not exist!\033[0m')


def repay(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' ------ Balance Info ------
        Credit :     %s
        Balance:     %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        repay_amount = input("\033[33;1mInput repay amount(input 'b' to exit):\033[0m").strip()
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'repay',repay_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        elif repay_amount == 'b':
            back_flag = True
        else:
            print('\033[31;1m[%s] is not a valid amount,only accept integer!\033[0m' % repay_amount)



def withdraw(acc_data):
    '''
    print current balance and let user do the withdraw action
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' ------ Balance Info ------
        Credit :     %s
        Balance:     %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        withdraw_amount = input('\033[33;1mInput withdraw amount:\033[0m').strip()
        if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'withdraw',withdraw_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount,only accept integer!\033[0m' % withdraw_amount)

        if withdraw_amount == 'b':
            back_flag = True


def transfer(acc_data):
    '''
    Transfers between accounts
    :param acc_data:
    :return:
    '''
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = ''' ------ Balance Info ------
        Credit :     %s
        Balance:     %s''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    back_flag = False
    while not back_flag:
        receiving_account = input('\033[33;1mInput Receiving Account("input "b" to exit"):\033[0m').strip()
        if receiving_account == 'b':
            back_flag = True
            continue
        transfer_amount = input('\033[33;1mInput transfer amount:\033[0m').strip()
        receiving_data = accounts.load_current_balance(receiving_account)

        if len(transfer_amount) > 0 and transfer_amount.isdigit():
            new_balance = transaction.make_transaction(trans_logger,account_data,'transfer',transfer_amount)
            new_receiving_balance = transaction.make_transaction(trans_logger,receiving_data,'collection',transfer_amount)
            if new_balance:
                print('''\033[42;1mNew Balance:%s\033[0m''' % (new_balance['balance']))
        else:
            print('\033[31;1m[%s] is not a valid amount,only accept integer!\033[0m' % transfer_amount)


def pay_check(acc_data):
    pass


def shopping_cart(acc_data):
    account_data = accounts.load_current_balance(acc_data['account_id'])
    current_balance = '''\033[33;1m------ Balance Info ------
        Credit :     %s
        Balance:     %s\033[0m''' % (account_data['credit'], account_data['balance'])
    print(current_balance)
    shoppingcart.shopping(account_data,trans_logger)


def logout(acc_data):
    account_id = acc_data['account_id']
    user_data['is_authenticated'] = False
    access_logger.info("account %s just log out ATM" % account_id)
    exit("user %s log out ATM..bye.." % account_id)