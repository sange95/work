#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

'''
Provide user specific data and interact with gate.io
'''

from gateAPI import GateIO

## 填写 apiKey APISECRET
apiKey = '62D1E239-38A3-4029-90EF-4A9CC745B8B6'
secretKey = 'e77cb948be92c6d1ab30e610b3dc2f228aae4ec824c1e0d9f3171728af4a7514'
## address
btcAddress = 'your btc address'


## Provide constants

API_QUERY_URL = 'data.gateio.io'
API_TRADE_URL = 'api.gateio.io'

## Create a gate class instance

gate_query = GateIO(API_QUERY_URL, apiKey, secretKey)
gate_trade = GateIO(API_TRADE_URL, apiKey, secretKey)


# Trading Pairs
print("返回所有系统支持的交易对")
print(gate_query.pairs())


## Below, use general methods that query the exchange

#  Market Info
print("返回所有系统支持的交易市场的参数信息，包括交易费，最小下单量，价格精度等")
print(gate_query.marketinfo())

# Market Details
print("返回所有系统支持的交易市场的详细行情和币种信息，包括币种名，市值，供应量，最新价格，涨跌趋势，价格曲线等")
print(gate_query.marketlist())

# Tickers
print("返回系统支持的所有交易对的 最新，最高，最低 交易行情和交易量，每10秒钟更新,如果后面添加具体的参数就是单个的币种的具体详情")
print(gate_query.tickers())
# Depth
print("返回系统支持的所有交易对的市场深度（委托挂单），其中 asks 是委卖单, bids 是委买单,如果后面有具体的参数则是具体币种的深度详情")
print(gate_query.orderBooks())

# orders
print("获取我的当前挂单列表API")
print(gate_query.openOrders())

# 下面的都是需要个人用户的秘钥的api,基本都是操作个人用户的api
## Below, use methods that make use of the users keys

# Ticker
print("具体交易的行情")
print(gate_query.ticker('btc_usdt'))

# Market depth of pair
print("交易对的市场深度")
print(gate_query.orderBook('btc_usdt'))

# Trade History
print("返回最新80条历史成交记录")
print(gate_query.tradeHistory('btc_usdt'))

# Get account fund balances
print("获取帐号资金余额API")
print(gate_trade.balances())

# get new address
print(gate_trade.depositAddres('btc'))

# get deposit withdrawal history
print(gate_trade.depositsWithdrawals('1469092370', '1569092370'))

# Place order sell
print(gate_trade.buy('etc_btc', '0.001', '123'))

# Place order sell
print(gate_trade.sell('etc_btc', '0.001', '123'))

# Cancel order
print(gate_trade.cancelOrder('267040896', 'etc_btc'))

# Cancel all orders
print(gate_trade.cancelAllOrders('0', 'etc_btc'))

# Get order status
print(gate_trade.getOrder('267040896', 'eth_btc'))

# Get my last 24h trades
print(gate_trade.mytradeHistory('etc_btc', '267040896'))

# withdraw
print(gate_trade.withdraw('btc', '88', btcAddress))
