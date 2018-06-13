from huobiservice import HuoBi


ACCESS_KEY = "215ed2c3-85a3f35b-53688e00-c81f2"
SECRET_KEY = "7a22b4d6-dea0d1cd-4cbbca1e-7ffd2"
BASE_URL = "https://api.huobi.pro"

obj = HuoBi(ACCESS_KEY, SECRET_KEY, BASE_URL)

print(50*"*")
print(obj.get_kline('btcusdt', '1min'))

print(50*"*")
print(obj.get_depth('btcusdt', 'step0'))

print(50*"*")
print(obj.get_trade('btcusdt'))

print(50*"*")
print(obj.get_ticker('btcusdt'))

print(50*"*")
print(obj.get_detail('btcusdt')) 

print(50*"*")
print(obj.get_symbols())

print(50*"*")
print(obj.get_balance())