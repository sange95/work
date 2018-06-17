from zbapi import *

access_key = '0d39053a-9734-448a-80c8-8e3f2b1ac1e8'
access_secret = '99f5af9f-ef53-4e3d-a2f0-5f1449250a67'
api = Client_Zb(access_key, access_secret)

# print(api.ticker())

# print(api.depth())

# print(api.balance())
# 余额不足
# print(api.trade("limit_sell", 1560, 0.1, "bcc_zb"))
#挂单没找到
# print(api.order_info('bcc_zb', '5264586'))
#撤单失败
# print(api.cancel_order('bcc_zb', 5264586))

# print(api.cancel_all())
# 内部错误
# print(api.open_orders("zb_usdt", "sell"))

# print(api.get_market())
# 服务器忙碌
# print(api.get_kline())

# print(api.get_trades('bcc_zb'))
# 挂单没找到
# print(api.get_order(25645, "bcc_zb"))
# 没有充值地址
# print(api.get_user_address("btc"))

# print(api.get_withdraw_address("btc"))

# print(api.get_withdraw_record("btc", 2, 20))

# print(api.get_charge_record("btc", 2, 20))
# 内部错误
# print(api.get_withdraw('btc', 0.1, 100, "jjjjjjjjjjjjj", 56155))

# print(api.getLeverAssetsInfo())

# print(api.getLeverBills("btc", 1, 2, 20))

# print(api.transferInLever("btc", 100, "市场名称"))

# print(api.transferOutLever("btc", 100, "市场名称"))

print(api.loan("btc", 100, 0.1, 20, 1))

print(api.cancelLoan(156425))

print(api.getLoans("btc", 2, 20))

print(api.getLoanRecords("btc", 2, 225640, "市场名称", 2))

print(api.borrow("btc", 100, 0.1, 20, 1, "市场名称"))

print(api.repay(55164, 1000, 1))

print(api.getRepayments(15664, 2, 100))

print(api.getFinanceRecords("btc", 2, 100))


