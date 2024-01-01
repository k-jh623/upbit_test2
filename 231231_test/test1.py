import time
import pyupbit
import datetime


###functions
def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

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
coin = "KRW-BSV"
coin_name = "BSV"
IR = 0.04
input = 5000
eth_amount = get_balance(coin_name)

continue_crt = True
while continue_crt:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(coin) # 시작시간
        end_time = start_time + datetime.timedelta(days = 1) # 시작시간 + 1일
        if start_time < now < end_time - datetime.timedelta(seconds=10): # 시작 ~ 마감 10초전

            current_price = get_current_price(coin)
            eth_amount = get_balance(coin_name)
            current_eth_price = current_price * eth_amount
            print("current budget: ", get_balance("KRW"))
            print("current eth_price: ", current_eth_price)

            upper_bound = input * (1+IR)
            lower_bound = input * (1-IR)

            print("upper_bound: ", upper_bound)
            print("lower_bound: ", lower_bound)

            if eth_amount == 0:
                input = 5000
                upbit.buy_market_order(coin, input)
                print("start!!")

            elif current_eth_price >= upper_bound: ## 가격 증가
                upbit.sell_market_order(coin, eth_amount) # 전량 판매
                print("up!!")
                print("sell eth_price: ", current_eth_price)
                
            elif current_eth_price <= lower_bound: # 가격 하락
                pre_input = input
                new_input = input*(1+IR) # 새로운 매입가 (마틴) = input*IR + current_eth_price + (input-current_eth_price) - input
                if pre_input >= 80000:
                    continue_crt = False
                    print("FAIL"*10)
                else:
                    upbit.buy_market_order(coin, new_input)
                    input = pre_input + new_input # input*IR + current_eth_price + (input-current_eth_price) + input
                    print("down!!")
                    print("buy eth_price: ", input)

        else: # 하루 끝
            eth = get_balance(coin_name)
            upbit.sell_market_order(coin, eth)
            continue_crt = False

        time.sleep(30)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue_crt = False



            


