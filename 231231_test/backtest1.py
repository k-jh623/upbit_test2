import pyupbit
import numpy as np
import time
import datetime

access = "e6fyMasXKnbRN6bZZRQ0QzZod0PuTK85xTOcRIsb"
secret = "AtXjWzCCrjXjnxIc7EEoB1k0hT3nqqFrHkf0wxu0"       
upbit = pyupbit.Upbit(access, secret)

###functions.
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

### params.
coin = "KRW-AQT"
coin_name = "AQT"
IR = 0.04
start_input = 5000
fee_rate = 0.0005
eth_amount = get_balance(coin_name)

### backtest.
df = pyupbit.get_ohlcv(coin, count=5000) # N일동안의 OHLCV 값을 불러옴

df['range'] = (df['open'] - df['open'].shift(1)) / (df['open'])

input = start_input
df['input'] = 0
df['input'].iloc[0] = input
df['value'] = 0
df['income'] = 0
df['cul_income'] = 0

for i in range(1, len(df)):
    inc_rate = df['range'].iloc[i]    
    df['input'].iloc[i] = input
    df['value'].iloc[i] = df['input'].iloc[i] + df['range'].iloc[i] * df['input'].iloc[i]

    input = df['input'].iloc[i]
    current_value = df['value'].iloc[i]

    if current_value >= input * (1+IR):
        input = 5000
        income = current_value - input # 1회 매도
        fee = current_value*fee_rate
        income = income - fee
        df['income'].iloc[i] = income

    elif current_value <= input * (1-IR):
        input = current_value + input*(1+IR) # 1회 매수
        fee = (input-current_value) * fee_rate
        income = income - fee

    df['cul_income'].iloc[i] = df['cul_income'].iloc[i-1] + df['income'].iloc[i]

print(df)
print(df['input'].max())
df.to_excel("dd.xlsx")






# # 매수가를 정하기 위한 코드
# # target (매수가)
# df['range'] = (df['high'] - df['low']) * 0.5 # 변동폭 (고가-저가) * k (0.5)
# df['target'] = df['open'] + df['range'].shift(1)  # 시가 + shift는 range 컬럼을 한칸씩 밑으로 내림
# print(df)

# fee = 0.05
# # ror (수익율)
# # np.where(조건문, 참일때 값, 거짓일때 값)
# df['ror'] = np.where(df['high'] > df['target'],
#                      df['close'] / df['target'] - fee, # 종가는 판매가
#                      1)
# # hpr (누적수익률)
# # draw down (하락폭) = 누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100
# df['hpr'] = df['ror'].cumprod()
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# print("MDD(%): ", df['dd'].max())
# df.to_excel("dd.xlsx")