#!/usr/bin/env python
# This program buys some Dogecoins and sells them for a bigger price
from bittrex import bittrex

# Get these from https://bittrex.com/Account/ManageApiKey
api = bittrex('4795cfda1f7b4af8926b846346462ba0', '9a61c8a46c914ce8ad17a7ab0a5ec6e0')

# Market to trade at
trade = 'BTC'
currency = 'DOGE'
market = '{0}-{1}'.format(trade, currency)
# Amount of coins to buy
amount = 100
# How big of a profit you want to make
multiplier = 1.1

Type = 'both'

# Getting the BTC price for DOGE
dogesummary = api.getmarketsummary(market)

dogeprice = dict(dogesummary[0])['Last']
print(dogeprice)
# print('The price for {0} is {1:.8f} {2}.'.format(currency, dogeprice, trade))

# Buying 100 DOGE for BTC
# print('Buying {0} {1} for {2:.8f} {3}.'.format(amount, currency, dogeprice, trade))
# api.buylimit(market, amount, dogeprice)

# Multiplying the price by the multiplier
# dogeprice = round(dogeprice*multiplier, 8)

# Selling 100 DOGE for the  new price
# print('Selling {0} {1} for {2:.8f} {3}.'.format(amount, currency, dogeprice, trade))
# api.selllimit(market, amount, dogeprice)

# Gets the DOGE balance
# dogebalance = api.getbalance(currency)
# print("Your balance is {0},{1}".format(str(dogebalance['Available']), str(currency)))

# For a full list of functions, check out bittrex.py or https://bittrex.com/Home/Api
# print("************************************************")
# print(api.getmarkets())
# print("************************************************")
# print(api.getcurrencies())
# print("************************************************")
# print(api.getticker(market))
# print("************************************************")
# print(api.getmarketsummaries)
# print("************************************************")
# print(dogesummary)
# print("************************************************")
# print(api.getorderbook(market, Type))
# print("************************************************")
# print(api.getmarkethistory(market))
# print(api.buylimit(market, amount, dogeprice))
# print("************************************************")
# print(api.selllimit(market, amount, dogeprice))
# print("************************************************")
# print(api.cancel("ldkjfbnghsfpdjfo"))
# print("************************************************")
# print(api.getopenorders(market))
# print("************************************************")
# print(api.getbalance(currency))
# print("************************************************")
# print(api.getbalances())
# print("************************************************")
# print(api.getdepositaddress(currency))
# print("************************************************")
# print(api.getorder("5555555"))
# print("************************************************")
# print(api.getorderhistory(market, 20))
# print("************************************************")
# print(api.getdeposithistory(currency, 20))

