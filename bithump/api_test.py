#! /usr/bin/env python
#
# @brief XCoin API-call sample script (for Python 2.x, 3.x)
#
# @author btckorea
# @date 2017-04-14
#
# @details
# First, Build and install pycurl with the following commands::
# (if necessary, become root)
#
# https://pypi.python.org/pypi/pycurl/7.43.0#downloads
#
# tar xvfz pycurl-7.43.0.tar.gz
# cd pycurl-7.43.0
# python setup.py --libcurl-dll=libcurl.so install
# python setup.py --with-openssl install
# python setup.py install
#
# @note
# Make sure current system time is correct.
# If current system time is not correct, API request will not be processed normally.
#
# rdate -s time.nist.gov
#

import sys
from bithumb import *
import pprint

rgParams = {
	"order_currency" : "BTC",
	"payment_currency" : "KRW"
}


api_key = "d11fd190a7154491ad82cfc30fc4acb1"
api_secret = "731d60e30a7b40d1b12ab67d7f9284d2"

api = XCoinAPI(api_key, api_secret)

# print(api.get_public_ticker())

# print(api.get_public_orderbook(params={'group_orders':1, 'count':3}))

# print(api.get_public_orderbook())

# print(api.get_transaction_history())

# print(api.get_account_info("BTC"))

# print(api.get_account_wallet_address())

# print(api.get_account_balance())

# print(api.get_account_ticker())

# print(api.get_account_orders(1417160401000))

# print(api.get_account_transactions(1, 0))

# print(api.get_trade_place(0.001, 1000, "ask"))
# 参数出错
# print(api.get_order_detail("55555", "ask"))
# 参数出错
# print(api.get_order_detail("45691254895544", "ask"))

# print(api.get_trade_krw_deposit())

# print(api.get_trade_buy(0.001))

# print(api.get_trade_sell(0.001))
