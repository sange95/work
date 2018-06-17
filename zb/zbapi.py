#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author:xuanzhi

import requests
import json
import time
import hashlib
import hmac
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode




BASE_API_PUBLIC = 'http://api.zb.com/data/v1'
BASE_API_PRIVATE = 'https://trade.zb.com/api'

DEFAULT_HEADERS = {'Content-Type': 'application/x-www-form-urlencode'}


proxies = {
    'https': 'http://127.0.0.1:1080',
    'http': 'http://127.0.0.1:1080'
}

class Client_Zb():
    def __init__(self, apikey, secretkey):
        self._public_key = str(apikey)
        self._private_key = str(secretkey)
        self.sessn = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(pool_connections=5,
                                                     pool_maxsize=5, max_retries=5)
        self.sessn.mount('http://', self.adapter)
        self.sessn.mount('https://', self.adapter)
        self.order_list = []

    def signature(self,message):
        sha_secretkey = hashlib.sha1(self._private_key.encode('utf-8')).hexdigest()
        signature = hmac.new(sha_secretkey.encode('utf-8'),message.encode('utf-8'),digestmod='MD5').hexdigest() # 32位md5算法进行加密签名
        return signature

    def signedRequest(self, method, path, params):

        # create signature:

        params['accesskey'] = self._public_key
        param = ''
        for key in sorted(params.keys()):
            #print(key)
            param += key + '=' + str(params.get(key)) + '&'
        param = param.rstrip('&')
        #print(param)
        signature = self.signature(message=param)
        #print(signature)
        params['sign'] = str(signature)
        params['reqTime'] = int(time.time() * 1000)
        print(params)
        resp = self.sessn.request(method,BASE_API_PRIVATE+path,headers=DEFAULT_HEADERS,data=None,params=params,proxies=proxies)
        print(resp.content)
        data = json.loads(resp.content)
        return data

    def ticker(self,symbol='eth_btc'):
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'market':symbol}
        url = BASE_API_PUBLIC + '/ticker'
        #print(url)
        resp = requests.request("GET",url,params=params,proxies=proxies)
        data = json.loads(resp.text)['ticker']
        return data

    def depth(self,symbol='eth_btc'):
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'market':symbol}
        url = BASE_API_PUBLIC + '/depth'
        resp = requests.request("GET",url,params=params,proxies=proxies)
        data = json.loads(resp.text)
        temp = {'asks':data['asks'][::-1],'bids':data['bids']}
        return temp
    # 待修改
    def balance(self):
        params = {'method':'getAccountInfo'}
        result = self.signedRequest(method="GET",path ='/getAccountInfo',params=params)
        resp = result['result']['coins']
        avalible,frozen,total = {},{},{}
        for item in resp:
            coin = item['enName']
            avalible[coin] = float(item['available'])
            frozen[coin] = float(item['freez'])
            total[coin] = avalible[coin] + frozen[coin]
        temp = {'total':total,'avalible':avalible,'frozen':frozen}
        return result

    def trade(self,trade_type,price,amount,symbol):
        '''
        只存在限价买卖，limit_buy/limit_sell
        对于成功的订单，返回该订单号，并将其存入订单列表，以便后续的查看与撤单

        '''
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')	
        params = {'method':'order'} 
        order_type,side = trade_type.split('_')
        params = {'currency':symbol,'price':price,'amount':amount, 'method': 'order'}
        if order_type == 'limit':
            if side == 'buy':
                params['tradeType'] = 1
            elif side == 'sell':
                params['tradeType'] = 0
        else:
            print('下单错误！！！')
        # params['method'] = "order"
        resp = self.signedRequest(method="GET",path ='/order',params=params)
        print(resp['code'])
        if resp['code'] == 1000:
            return resp['id']
            self.order_list.append(resp['id'])
        else:
            print('下单失败！！！')


    def order_info(self,symbol,order_id):
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'id':order_id,'currency':symbol,'method':'getOrder'}
        resp = self.signedRequest(method="GET",path ='/getOrder',params=params)
        return resp

    def cancel_order(self,symbol,order_id):
        '''
        传入订单Id与交易对，如撤单成功则打印‘撤单成功’，如撤单失败则打印撤单失败并返回失败的Id
        '''
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'id':order_id,'currency':symbol,'method':'ancelOrder'}
        resp = self.signedRequest(method="GET",path ='/cancelOrder',params=params)
        if resp['code'] == 1000:
            print('撤单成功: ',order_id)
            self.order_list.remove(order_id)
        else:
            print('撤单失败: ',order_id)
            return order_id

    def cancel_all(self):
        '''
            返回所有处理过的订单id,无论成功失败。
        '''
        orderid_list=self.order_list
        processed_id = [] 
        for i in orderid_list:
             processed_id.append(self.cancel_order("btc", i))
        return processed_id

    def open_orders(self,symbol,side,pageIndex=1):
        '''
            获取多个委托买单或卖单，每次请求返回10条记录
            side: 可选 buy 1 /sell 0
            pageIndex:记录页数
        '''
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'currency':symbol,'tradeType':side,'pageIndex':pageIndex,'method':'getOrdersNew'}
        resp = self.signedRequest(method="GET",path='/getOrdersNew',params=params)
        return resp

    def get_market(self):
        resp = requests.get(BASE_API_PUBLIC + '/markets')
        return json.loads(resp.content)

    def get_kline(self, symbol=None):

        if symbol:
            url = BASE_API_PUBLIC + '/kline?symbol=' + symbol
            symbol = symbol.lower()
            if 'usd' in symbol:
                symbol = symbol.replace('usd', 'usdt')
        else:
            url = BASE_API_PUBLIC + '/kline'
        print(url)
        resp = requests.get(url)
        print(resp.content)
        return json.loads(resp.content)


    def get_trades(self, markets=None):

        if markets:
            url = BASE_API_PUBLIC + '/trades?market=' + markets
            markets = markets.lower()
            if 'usd' in markets:
                markets = markets.replace('usd', 'usdt')
        else:
            url = BASE_API_PUBLIC + '/trades'
        print(url)
        resp = requests.get(url)
        print(resp.content)
        return json.loads(resp.content)

    def get_order(self, id, symbol):

        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'currency':symbol,'id':id,'method':'getOrder'}
        resp = self.signedRequest(method="GET",path='/getOrder',params=params)
        return resp

    def get_user_address(self, symbol):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getUserAddress', 'currency': symbol}
        resp = self.signedRequest(method="GET",path='/getUserAddress',params=params)
        return resp

    def get_withdraw_address(self, symbol):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getWithdrawAddress', 'currency': symbol}
        resp = self.signedRequest(method="GET",path='/getWithdrawAddress',params=params)
        return resp


    def get_withdraw_record(self, symbol, pageIndex, pageSize=10):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getWithdrawRecord', 'currency': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize}
        resp = self.signedRequest(method="GET",path='/getWithdrawRecord',params=params)
        return resp

    def get_charge_record(self, symbol, pageIndex, pageSize=10):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getChargeRecord', 'currency': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize}
        resp = self.signedRequest(method="GET",path='/getChargeRecord',params=params)
        return resp


    def get_withdraw(self, symbol, account, fees, receiveAddr, safePwd, itransfer=False):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'withdraw', 'currency': symbol, 'account': account, 'fees': fees, 'receiveAddr': receiveAddr, 'safePwd': safePwd, 'itransfer': itransfer}
        resp = self.signedRequest(method="GET",path='/withdraw',params=params)
        return resp

    def getLeverAssetsInfo(self):
        
        params = {'method':'getLeverAssetsInfo'}
        resp = self.signedRequest(method="GET",path='/getLeverAssetsInfo',params=params)
        return resp
    
    def getLeverBills(self, symbol, dataType, pageIndex, pageSize=10):  
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getLeverBills', 'coin': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize, 'dataType': dataType}
        resp = self.signedRequest(method="GET",path='/getLeverBills',params=params)
        return resp

    def transferInLever(self, symbol, amount, marketName):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'transferInLever', 'currency': symbol, 'amount': amount, 'marketName': marketName}
        resp = self.signedRequest(method="GET",path='/transferInLever',params=params)
        return resp

    def transferOutLever(self, symbol, amount, marketName):
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'transferOutLever', 'currency': symbol, 'amount': amount, 'marketName': marketName}
        resp = self.signedRequest(method="GET",path='/transferOutLever',params=params)
        return resp

    def loan(self, symbol, amount, interestRateOfDay, repaymentDay, isLoop):
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'loan', 'currency': symbol, 'amount': amount, 'interestRateOfDay': interestRateOfDay, 'repaymentDay': repaymentDay,'isLoop': isLoop}
        resp = self.signedRequest(method="GET",path='/loan',params=params)
        return resp
    
    def cancelLoan(self, loanId):
        params = {'method':'cancelLoan', 'loanId': loanId}
        resp = self.signedRequest(method="GET",path='/cancelLoan',params=params)
        return resp
    
    def getLoans(self, symbol, pageIndex, pageSize=10):  
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getLoans', 'coin': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize}
        resp = self.signedRequest(method="GET",path='/getLoans',params=params)
        return resp
    
    def getLoanRecords(self, symbol, status, loanId, marketName, pageIndex, pageSize=10):  
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getLoanRecords', 'coin': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize, 'status': status, 'loanId': loanId, 'marketName': marketName}
        resp = self.signedRequest(method="GET",path='/getLoanRecords',params=params)
        return resp
    
    def borrow(self, symbol, amount, interestRateOfDay, repaymentDay, isLoop, marketName):
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'borrow', 'coin': symbol, 'amount': amount, 'interestRateOfDay': interestRateOfDay, 'repaymentDay': repaymentDay,'isLoop': isLoop, 'marketName': marketName}
        resp = self.signedRequest(method="GET",path='/borrow',params=params)
        return resp
    def repay(self, loanRecordId, repayAmount, repayType):

        params = {'method':'repay', 'loanRecordId': loanRecordId, 'repayType': repayType, 'repayAmount': repayAmount}
        resp = self.signedRequest(method="GET",path='/repay',params=params)
        return resp
    
    def getRepayments(self, loanRecordId, pageIndex, pageSize=10):  
        
        params = {'method':'getRepayments', 'loanRecordId': loanRecordId, 'pageIndex': pageIndex, 'pageSize': pageSize}
        resp = self.signedRequest(method="GET",path='/getRepayments',params=params)
        return resp

    def getFinanceRecords(self, symbol, pageIndex, pageSize=10):  
        
        symbol = symbol.lower()
        if 'usd' in symbol:
            symbol = symbol.replace('usd','usdt')
        params = {'method':'getFinanceRecords', 'coin': symbol, 'pageIndex': pageIndex, 'pageSize': pageSize}
        resp = self.signedRequest(method="GET",path='/getFinanceRecords',params=params)
        return resp

