from gdax import *


api = PublicClient()

# 平台中注册成功了但是卡在了基本信息填写过程中，以至于无法获得api
# auth_api = AuthenticatedClient()


print(api.get_products())

print(api.get_product_order_book('BTC-USD'))

print(api.get_product_trades('BTC-USD'))

print(api.get_currencies())

print(api.get_product_24hr_stats('BTC-USD'))

print(api.get_product_historic_rates('BTC-USD'))

print(api.get_time())