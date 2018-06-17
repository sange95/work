import hmac
import hashlib
import json, requests
import random

class Bibox:
    BASE_URL = " https://api.bibox.com/v1/"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def getSign(self, data):
        result = hmac.new(self.api_secret.encode("utf-8"), data.encode("utf-8"), hashlib.md5).hexdigest()
        return result

    def doApiRequestWithApikey(self, url, cmds):
        s_cmds = json.dumps(cmds)
        sign = self.getSign(s_cmds)
        r = requests.post(url, data={'cmds': s_cmds, 'apikey': self.api_key,'sign':sign})
        return json.loads(r.content)

    def doApiRequestNoApikey(self, url, cmds):
        s_cmds = json.dumps(cmds)
        r = requests.post(url, data={'cmds': s_cmds})
        return json.loads(r.content)

    def assets(self, symbol=None):
        url = self.BASE_URL + "transfer"
        print(url)
        cmds = [{
            'cmd':"transfer/assets",
            'body':{
                "select": "BTC"
            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    def pairList(self):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/pairList",
            'body':{}
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def kline(self, pair, period, size=1000):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/kline",
            'body':{
                'pair': pair,
                'period': period,
                'size': size
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def marketAll(self):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/marketAll",
            'body':{
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def market(self, pair):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/market",
            'body':{
                'pair': pair
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def depth(self, pair, size=200):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/depth",
            'body':{
                'pair': pair,
                'size': size
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def deals(self, pair, size=200):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/deals",
            'body':{
                'pair': pair,
                'size': size
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)

    def ticker(self, pair):
        url = self.BASE_URL + "mdata"
        cmds = [{
            'cmd':"api/ticker",
            'body':{
                'pair': pair
            }
        }]
        return self.doApiRequestNoApikey(url, cmds)
    
    def withdrawInfo(self, id):
        url = self.BASE_URL + "transfer"
        cmds = [{
            'cmd':"transfer/withdrawInfo",
            'body':{
                'id': id
            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    def trade(self, pair, account_type, order_type, order_side, pay_bix, price, amount, money):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/trade",
            'index': random.randint(10000, 99999),
            'body':{
                'pair': pair,
                'account_type': account_type,
                'order_type': order_type,
                'order_side': order_side,
                'pay_bix': pay_bix,
                'price': price,
                'amount': amount,
                'money': money

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    
    def cancel_trade(self, orders_id):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/cancelTrade",
            'index': random.randint(10000, 99999),
            'body':{
                'orders_id': orders_id

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    
    def orderPendingList(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/orderPendingList",
            'index': random.randint(10000, 99999),
            'body':{
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'order_side': order_side,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    def pendingHistoryList(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side, hide_cancel):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/pendingHistoryList",
            'index': random.randint(10000, 99999),
            'body':{
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'order_side': order_side,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol,
                'hide_cancel': hide_cancel

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    def delegation_order(self, id):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/order",
            'body':{
                'id': id

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)

    def orderHistoryList(self, pair, account_type, page, size, coin_symbol, currency_symbol, order_side):
        url = self.BASE_URL + "orderpending"
        cmds = [{
            'cmd':"orderpending/orderHistoryList",
            'body':{
                'pair': pair,
                'account_type': account_type,
                'page': page,
                'order_side': order_side,
                'size': size,
                'coin_symbol': coin_symbol,
                'currency_symbol': currency_symbol

            }
        }]
        return self.doApiRequestWithApikey(url, cmds)


api_key = '080a06db9d002c275b05c9f7a959fe17a76c1dd1'
api_secret = 'ea95f832a5789f3a96c605941a6c70523ff959fa'


api = Bibox(api_key, api_secret)
# print(api.assets())

# print(api.pairList())

# print(api.withdrawInfo(228))

# print(api.trade("ELF_BTC", 0, 1, 1, 1, 200, 0.001, 3000))

# print(api.cancel_trade(56428))

# print(api.orderPendingList("ELF_BTC", 0, 1, 1, 'BTC', 'ETH', 1))

# print(api.pendingHistoryList("ELF_BTC", 0, 1, 1, 'BTC', 'ETH', 1, 0))

# print(api.delegation_order(54682))

# print(api.orderHistoryList("ELF_BTC", 0, 1, 1, 'BTC', 'ETH', 1))

# print(api.kline("ELF_BTC", "1min"))

# print(api.ticker("ELF_BTC"))

# print(api.depth("ELF_BTC", 100))

# print(api.deals("ELF_BTC", 100))

# print(api.marketAll())



