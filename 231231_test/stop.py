import time
import pyupbit
import datetime
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--coin_name', required=True)
args = parser.parse_args()

###functions
def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


### 보유 현금 조회
access = "e6fyMasXKnbRN6bZZRQ0QzZod0PuTK85xTOcRIsb"
secret = "AtXjWzCCrjXjnxIc7EEoB1k0hT3nqqFrHkf0wxu0"       
upbit = pyupbit.Upbit(access, secret)


### 보유 현금 조회
coin = args.coin_name
coin_name = coin[4:]
eth_amount = get_balance(coin_name)
upbit.sell_market_order(coin, eth_amount) # 전량 판매