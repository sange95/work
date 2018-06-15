import sys
import time
import math
import base64
import hmac, hashlib

PY3 = sys.version_info[0] > 2
if PY3:
	import urllib.parse
else:
	import urllib

import pycurl
import json
import certifi
import requests
import io


class XCoinAPI:
	api_url = "https://api.bithumb.com"
	api_key = "d11fd190a7154491ad82cfc30fc4acb1"
	api_secret = "731d60e30a7b40d1b12ab67d7f9284d2"

	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret
		self.bytes_handle = io.BytesIO()

	def microtime(self, get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def microsectime(self) :
		mt = self.microtime(False)
		mt_array = mt.split(" ")[:2]
		return mt_array[1] + mt_array[0][2:5]

	def xcoinApiCall(self, endpoint, rgParams):
		# 1. Api-Sign and Api-Nonce information generation.
		# 2. Request related information from the Bithumb API server.
		#
		# - nonce: it is an arbitrary number that may only be used once. (Microseconds)
		# - api_sign: API signature information created in various combinations values.
		bytes_handle = io.BytesIO()
		endpoint_item_array = {
			"endpoint" : endpoint
		}

		uri_array = dict(endpoint_item_array, **rgParams) # Concatenate the two arrays.
		if PY3:
			e_uri_data = urllib.parse.urlencode(uri_array)
		else:
			e_uri_data = urllib.urlencode(uri_array)

		# Api-Nonce information generation.
		nonce = self.microsectime()

		# Api-Sign information generation.
		hmac_key = self.api_secret
		utf8_hmac_key = hmac_key.encode('utf-8')

		hmac_data = endpoint + chr(0) + e_uri_data + chr(0) + nonce
		utf8_hmac_data = hmac_data.encode('utf-8')

		hmh = hmac.new(bytes(utf8_hmac_key), utf8_hmac_data, hashlib.sha512)
		hmac_hash_hex_output = hmh.hexdigest()
		utf8_hmac_hash_hex_output = hmac_hash_hex_output.encode('utf-8')
		utf8_hmac_hash = base64.b64encode(utf8_hmac_hash_hex_output)

		api_sign = utf8_hmac_hash
		utf8_api_sign = api_sign.decode('utf-8')

		# Connects to Bithumb API server and returns JSON result value.
		curl_handle = pycurl.Curl()
		curl_handle.setopt(pycurl.CAINFO, certifi.where())
		curl_handle.setopt(pycurl.POST, 1)
		#curl_handle.setopt(pycurl.VERBOSE, 1); # vervose mode :: 1 => True, 0 => False
		curl_handle.setopt(pycurl.POSTFIELDS, e_uri_data)

		url = self.api_url + endpoint
		curl_handle.setopt(curl_handle.URL, url)
		curl_handle.setopt(curl_handle.HTTPHEADER, ['Api-Key: ' + self.api_key, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce])
		
		curl_handle.setopt(curl_handle.WRITEFUNCTION, bytes_handle.write)
		curl_handle.perform()

		#response_code = curl_handle.getinfo(pycurl.RESPONSE_CODE); # Get http response status code.

		curl_handle.close()

		data = bytes_handle.getvalue()
		bytes_handle.close()

		return (json.loads(data))


	def _http_post_request(self, url, params=None, add_to_headers=None):
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
		
	def _http_get_request(self, url, params, add_to_headers=None):
		headers = {
			"Content-type": "application/x-www-form-urlencoded",
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
			}
		if add_to_headers:
			headers.update(add_to_headers)

		if params:
			postdata = urllib.parse.urlencode(params)
			response = requests.get(url, postdata, headers=headers, timeout=5) 
		else:
			response = requests.get(url, headers=headers, timeout=5) 
		try:
			if response.status_code == 200:
				return response.json()
			else:
				return
		except BaseException as e:
			print("httpGet failed, detail is:%s,%s" %(response.text,e))
		return
		
	def get_public_ticker(self, params=None, currency=None):

		url = self.api_url + '/public/ticker/' + currency if currency else self.api_url + '/public/ticker'
		return self._http_post_request(url, params)


	def get_public_orderbook(self, params=None, currency=None):

		url = self.api_url + '/public/orderbook/' + currency if currency else self.api_url + '/public/orderbook'
		return self._http_get_request(url, params)

	def get_transaction_history(self, params=None, currency=None):

		url = self.api_url + '/public/transaction_history/' if currency else self.api_url + '/public/transaction_history'

		return self._http_get_request(url, params)


	def get_account_info(self, currency=None):

		endpoint = "/info/account"
		parmas = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"currency": currency if currency else "BTC"	
		}

		return self.xcoinApiCall(endpoint, parmas)

	def get_account_balance(self, currency=None):

		endpoint = "/info/balance"
		params = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"currency": currency if currency else "BTC"
		}

		return self.xcoinApiCall(endpoint, params)


	def get_account_wallet_address(self, currency=None):

		endpoint = "/info/wallet_address"
		parmas = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"currency": currency if currency else "BTC"
		}

		return self.xcoinApiCall(endpoint, parmas)
	

	def get_account_ticker(self, currency=None):

		endpoint = "/info/ticker"
		parmas = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"order_currency": currency if currency else "BTC",
			"payment_currency": "KRW"
		}

		return self.xcoinApiCall(endpoint, parmas)

	
	def get_account_orders(self, after, order_id, t, count=100, currency="BTC"):

		endpoint = "/info/orders"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"order_id": order_id,
			"type": t,
			"count": count,
			"after": after,
			"currency": currency
		}
		return self.xcoinApiCall(endpoint, data)


	def get_account_transactions(self, offset, searchGb, count=20, currency="BTC"):

		endpoint = "/info/user_transactions"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"offset": offset,
			"searchGb": searchGb,
			"count": count,
			"currency": currency
		}
		return self.xcoinApiCall(endpoint, data)

	def get_trade_place(self, units, price, t, currency="BTC"):

		endpoint = "/trade/place"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"units": units,
			"type": t,
			"price": price,
			"order_currency": currency,
			"Payment_currency": "KRW"
		}
		return self.xcoinApiCall(endpoint, data)
	# 参数出错
	def get_order_detail(self, order_id, t, currency="BTC"):

		endpoint = "/info/order_detail"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"order_id": "12564856",
			"type": "ask",
			"currency": currency
		}
		print(data)
		return self.xcoinApiCall(endpoint, data)

	# 参数出错
	def get_trade_cancel(self, order_id, t, currency="BTC"):

		endpoint = "/trade/cancel"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"order_id": order_id,
			"type": t,
			"currency": currency
		}
		print(data)
		return self.xcoinApiCall(endpoint, data)

	
	def get_trade_withdrawal(self, units, price, address, destination, currency="BTC"):

		endpoint = "/trade/btc_withdrawal"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"units": units,
			"address": address,
			"price": price,
			"destination": currency,
			"Payment_currency": "KRW"
		}
		return self.xcoinApiCall(endpoint, data)

	
	def get_trade_krw_deposit(self):

		endpoint = "/trade/krw_deposit"
		parmas = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
		}

		return self.xcoinApiCall(endpoint, parmas)

	def get_trade_krw_withdrawal(self, bank, account, price):

		endpoint = "/trade/krw_withdrawal"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"bank": bank,
			"account": account,
			"price": price
		}
		return self.xcoinApiCall(endpoint, data)

	
	def get_trade_buy(self, units, currency="BTC"):

		endpoint = "/trade/market_buy"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"units": units,
			"currency": currency
		}
		return self.xcoinApiCall(endpoint, data)

	def get_trade_sell(self, units, currency="BTC"):

		endpoint = "/trade/market_sell"

		data = {
			"apikey": self.api_key,
			"secretkey": self.api_secret,
			"units": units,
			"currency": currency
		}
		return self.xcoinApiCall(endpoint, data)
