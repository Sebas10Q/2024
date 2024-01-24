from backtesting import Backtest, Strategy
from backtesting.test import SMA, GOOG
from backtesting.lib import crossover
import talib
import pandas as pd
import datetime
import numpy as np
import os
from upstox_api.api import *
from tempfile import gettempdir
from time import sleep, gmtime, strftime
import json

def SMA(x, n):
    z = talib.SMA(x['Close'], n).iloc[-1]
    return z

def ATR(x, n):
    z = talib.ATR(x['High'], x['Low'], x['Close'], timeperiod=14)
    return z

# =========================================================

filename = os.path.join(gettempdir(), 'interactive_api.json')
with open(filename) as f:
    key = json.loads(f.read())

with open('stock_symbols.txt') as f:
    sim = json.loads(f.read())

u = Upstox(key['api_key'], key['access_token'])
u.get_master_contract('NSE_EQ')
sym = sim

cols = ['Symbol', 'OPEN', 'HIGH', 'LOW', 'LTP', 'VOLUME_M', 'St1', 'CROSS']

df = pd.DataFrame(columns=cols)
df.Symbol = sym
df.set_index('Symbol', inplace=True)
df.fillna(0)

for count, i in enumerate(sym):
    try:
        x = u.get_ohlc(u.get_instrument_by_symbol('NSE_EQ', i), OHLCInterval.Day_1,
                       datetime.date.today() - datetime.timedelta(365), datetime.date.today())
        y = pd.DataFrame(x)
        y = y.apply(pd.to_numeric, args=('coerce',))
        y['timestamp'] = pd.to_datetime(pd.to_numeric(y['timestamp']) / 1000, unit='s') + pd.DateOffset(hours=5,
                                                                                                        minutes=30)
        y['timestamp'] = y.timestamp.dt.strftime('%d-%m-%Y')# %H:%M:%S')

        y.to_csv('data/{}.csv'.format(i))
        print('Fetched data of {}'.format(i))
    except:
        print('Failed to fetch data of stock: {}'.format(i))
        continue
sleep(2)