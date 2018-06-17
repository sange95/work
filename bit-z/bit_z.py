import math
import requests
import json
import time
import hashlib
import hmac
import random


class BitZ(object):
    BASE_URL = "https://www.bit-z.com"
    API_KEY = ""
    API_SECRET = ""

    def __init__(self, API_KEY, API_SECRET):

        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def do_signature(self, signature_str):
        a = signature_str + self.API_SECRET
        signature = hashlib.md5(a.encode('utf-8')).hexdigest()

        return signature

    def signature_post(self, parmas, url):
        parmas['api_key'] = self.API_KEY
        parmas['nonce'] = str(random.randint(100000, 999999))
        parmas['timestamp'] = int(time.time())

        signature_str = ''

        for key in sorted(parmas.keys()):
            signature_str += key + '=' + str(parmas.get(key)) + '&'

        signature_str = signature_str.rstrip('&')
        signature = self.do_signature(signature_str)
        parmas['sign'] = signature
        resp = requests.post(url, data=parmas)

        return json.loads(resp.content)

    def request_get(self, url, params={}):

        resp = requests.get(url, params=params)
        return json.loads(resp.content)

    def get_kline(self, params):
        url = self.BASE_URL + '/api_v1/kline'

        return self.request_get(url, params=params)

    def get_balance(self):
        url = self.BASE_URL + '/api_v1/balances'

        return self.signature_post({}, url)

    def get_open_order(self, params):
        url = self.BASE_URL + '/api_v1/openOrders'

        return self.signature_post(params, url)

    def cancel_order(self, params):
        url = self.BASE_URL + '/api_v1/tradeCancel'

        return self.signature_post(params, url)

    def trade_Add(self, params):
        url = self.BASE_URL + '/api_v1/tradeAdd'

        return self.signature_post(params, url)

    def get_trade_all(self):
        url = self.BASE_URL + '/api_v1/tickerall'

        return self.request_get(url)

    def get_depth(self, params):
        url = self.BASE_URL + '/api_v1/depth'

        return self.request_get(url, params=params)

    def get_ticker(self, params):
        url = self.BASE_URL + '/api_v1/ticker'

        return self.request_get(url, params=params)

    def get_orders(self, params):
        url = self.BASE_URL + '/api_v1/orders'

        return self.request_get(url, params=params)



api_key = 'f18d85becded352a1163b0fd4071e0f6'
api_secret = 'ScdhwOchmcNPsEB4eq1iisyzFF2RgTNfoMZi52s8OxOHYLCxAqomTHkN8HCDhX4U'

api = BitZ(api_key, api_secret)

print(api.get_kline({'coin': 'eth_btc','type': '1m'}))

print(api.get_balance())

print(api.get_open_order({'coin': 'eth_btc'}))

print(api.cancel_order({'id': '15648'}))

print(api.trade_Add({'type': 'in', 'price': 100, 'number': 0.1, 'coin': 'ltc_btc', 'tradepwd': '123456'}))

print(api.get_trade_all())

print(api.get_depth({'coin': 'lsk_btc'}))

print(api.get_ticker({'coin': 'lsk_btc'}))

print(api.get_orders({'coin': 'lsk_btc'}))

