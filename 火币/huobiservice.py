import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests


class HuoBi():
    def __init__(self, access_key, secret_key, base_url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.account_id = self.get_accounts()['data'][0]['id']

    

    def _http_get_request(self, url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        response = requests.get(url, postdata, headers=headers, timeout=5) 
        try:
            
            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpGet failed, detail is:%s,%s" %(response.text,e))
            return


    def _http_post_request(self, url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        response = requests.post(url, postdata, headers=headers, timeout=10)
        try:
            
            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpPost failed, detail is:%s,%s" %(response.text,e))
            return

    def _api_key_get(self, params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.access_key,
                    'SignatureMethod': 'HmacSHA256',
                    'SignatureVersion': '2',
                    'Timestamp': timestamp})

        host_name = urllib.parse.urlparse(self.base_url).hostname
        host_name = host_name.lower()
        params['Signature'] = self._createSign(params, method, host_name, request_path)

        url = self.base_url + request_path
        return self._http_get_request(url, params)


    def _api_key_post(self, params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.access_key,
                        'SignatureMethod': 'HmacSHA256',
                        'SignatureVersion': '2',
                        'Timestamp': timestamp}

        host_url = self.base_url
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self._createSign(params_to_sign, method, host_name, request_path)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self._http_post_request(url, params)


    def _createSign(self, pParams, method, host_url, request_path):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = self.secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature


    def get_accounts(self):
        """
        :return: 
        """
        path = "/v1/account/accounts"
        params = {}
        return self._api_key_get(params, path)

    
    def get_kline(self, symbol, period, size=150):
        """
        :param symbol
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size: 可选值： [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                'period': period,
                'size': size}

        url = self.base_url + '/market/history/kline'
        return self._http_get_request(url, params)

    # 获取marketdepth
    def get_depth(self, symbol, type):
        """
        :param symbol
        :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        params = {'symbol': symbol,
                'type': type}
        
        url = self.base_url + '/market/depth'
        return self._http_get_request(url, params)

    # 获取tradedetail
    def get_trade(self, symbol):
        """
        :param symbol
        :return:
        """
        params = {'symbol': symbol}

        url = self.base_url + '/market/trade'
        return self._http_get_request(url, params)

    
    # 获取merge ticker
    def get_ticker(self, symbol):
        """
        :param symbol: 
        :return:
        """
        params = {'symbol': symbol}

        url = self.base_url + '/market/detail/merged'
        return self._http_get_request(url, params)


    # 获取 Market Detail 24小时成交量数据
    def get_detail(self, symbol):
        """
        :param symbol
        :return:
        """
        params = {'symbol': symbol}

        url = self.base_url + '/market/detail'
        return self._http_get_request(url, params)

    # 获取支持的交易对
    def get_symbols(self, long_polling=None):
        """

        """
        params = {}
        if long_polling:
            params['long-polling'] = long_polling
        path = '/v1/common/symbols'
        return self._api_key_get(params, path)
    
    # 获取当前账户资产包含了所有的币种
    def get_balance(self):
        """
        :param acct_id
        :return:
        """
        
        if not self.account_id:
            self.account_id = self.get_accounts()['data'][0]['id']

        url = "/v1/account/accounts/{0}/balance".format(self.account_id)
        params = {"account-id": self.account_id}
        return self._api_key_get(params, url)

    
    # 创建并执行订单
    def send_order(self, amount, source, symbol, _type, price=0):
        """
        :param amount: 
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param symbol: 
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price: 
        :return: 
        """
        try:
            if not self.account_id:
                self.account_id = self.get_accounts()['data'][0]
        except BaseException as e:
            print ('get acct_id error.%s' % e)
        params = {"account-id": self.account_id,
                "amount": amount,
                "symbol": symbol,
                "type": _type,
                "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self._api_key_post(params, url)


    # 撤销订单
    def cancel_order(self, order_id):
        """
        
        :param order_id: 
        :return: 
        """
        params = {}
        url = "/v1/order/orders/{0}/submitcancel".format(order_id)
        return self._api_key_post(params, url)


    # 查询某个订单
    def order_info(self, order_id):
        """
        
        :param order_id: 
        :return: 
        """
        params = {}
        url = "/v1/order/orders/{0}".format(order_id)
        return self._api_key_get(params, url)


    # 查询某个订单的成交明细
    def order_matchresults(self, order_id):
        """
        
        :param order_id: 
        :return: 
        """
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(order_id)
        return self._api_key_get(params, url)


    # 查询当前委托、历史委托
    def orders_list(self, symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """
        
        :param symbol: 
        :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date: 
        :param end_date: 
        :param _from: 
        :param direct: 可选值{prev 向前，next 向后}
        :param size: 
        :return: 
        """
        params = {'symbol': symbol,
                'states': states}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        return self._api_key_get(params, url)


    # 查询当前成交、历史成交
    def orders_matchresults(self, symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """
        
        :param symbol: 
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date: 
        :param end_date: 
        :param _from: 
        :param direct: 可选值{prev 向前，next 向后}
        :param size: 
        :return: 
        """
        params = {'symbol': symbol}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/matchresults'
        return self._api_key_get(params, url)



    # 申请提现虚拟币
    def withdraw(self, address, amount, currency, fee=0, addr_tag=""):
        """

        :param address_id: 
        :param amount: 
        :param currency:btc, ltc, bcc, eth, etc ...(火币Pro支持的币种)
        :param fee: 
        :param addr-tag:
        :return: {
                "status": "ok",
                "data": 700
                }
        """
        params = {'address': address,
                'amount': amount,
                "currency": currency,
                "fee": fee,
                "addr-tag": addr_tag}
        url = '/v1/dw/withdraw/api/create'

        return self._api_key_post(params, url)

    # 申请取消提现虚拟币
    def cancel_withdraw(self, address_id):
        """

        :param address_id: 
        :return: {
                "status": "ok",
                "data": 700
                }
        """
        params = {}
        url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address_id)

        return self._api_key_post(params, url)


    '''
    借贷API
    '''

    # 创建并执行借贷订单


    def send_margin_order(self, amount, source, symbol, _type, price=0):
        """
        :param amount: 
        :param source: 'margin-api'
        :param symbol: 
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price: 
        :return: 
        """
        try:
            if not self.account_id:
                self.account_id = self.get_accounts()['data'][0]
        except BaseException as e:
            print ('get acct_id error.%s' % e)

        params = {"account-id": self.account_id,
                "amount": amount,
                "symbol": symbol,
                "type": _type,
                "source": 'margin-api'}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self._api_key_post(params, url)

    # 现货账户划入至借贷账户


    def exchange_to_margin(self, symbol, currency, amount):
        """
        :param amount: 
        :param currency: 
        :param symbol: 
        :return: 
        """
        params = {"symbol": symbol,
                "currency": currency,
                "amount": amount}

        url = "/v1/dw/transfer-in/margin"
        return self._api_key_post(params, url)

    # 借贷账户划出至现货账户


    def margin_to_exchange(self, symbol, currency, amount):
        """
        :param amount: 
        :param currency: 
        :param symbol: 
        :return: 
        """
        params = {"symbol": symbol,
                "currency": currency,
                "amount": amount}

        url = "/v1/dw/transfer-out/margin"
        return self._api_key_post(params, url)

    # 申请借贷
    def get_margin(self, symbol, currency, amount):
        """
        :param amount: 
        :param currency: 
        :param symbol: 
        :return: 
        """
        params = {"symbol": symbol,
                "currency": currency,
                "amount": amount}
        url = "/v1/margin/orders"
        return self._api_key_post(params, url)

    # 归还借贷
    def repay_margin(self, order_id, amount):
        """
        :param order_id: 
        :param amount: 
        :return: 
        """
        params = {"order-id": order_id,
                "amount": amount}
        url = "/v1/margin/orders/{0}/repay".format(order_id)
        return self._api_key_post(params, url)

    # 借贷订单
    def loan_orders(self, symbol, currency, start_date="", end_date="", start="", direct="", size=""):
        """
        :param symbol: 
        :param currency: 
        :param direct: prev 向前，next 向后
        :return: 
        """
        params = {"symbol": symbol,
                "currency": currency}
        if start_date:
            params["start-date"] = start_date
        if end_date:
            params["end-date"] = end_date
        if start:
            params["from"] = start
        if direct and direct in ["prev", "next"]:
            params["direct"] = direct
        if size:
            params["size"] = size
        url = "/v1/margin/loan-orders"
        return self._api_key_get(params, url)


    # 借贷账户详情,支持查询单个币种
    def margin_balance(self, symbol):
        """
        :param symbol: 
        :return: 
        """
        params = {}
        url = "/v1/margin/accounts/balance"
        if symbol:
            params['symbol'] = symbol
        
        return self._api_key_get(params, url)

