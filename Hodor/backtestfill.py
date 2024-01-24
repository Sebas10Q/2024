import pandas as pd
import talib
from binance.client import Client
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np
api_key = 'x7DDr5lM7AMxKPgS0hpw9faHsh18N3UFePHuSj7rQKXQoF0DqmzfIheYGSK2dRmr'
api_secret = 'I84PJAWizPwWcWRD0FsQ11KFLPOUq5evzq4543G1UvGTTcvHtqAZC0nmndK2PSqG'
# Initialize the Binance client
#api_key = 'your_api_key'
#api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

def get_binance_data(symbol, interval, start_str):
    df = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_str)
    df = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df.set_index('Open time', inplace=True)
    df = df.astype(float)
    return df
class MACDStrategy(Strategy):

    fastperiod = 12
    slowperiod = 26
    signalperiod = 9

    fastk_period = 14
    slowk_period = 3
    slowd_period = 3

    stock_threshold_buy = 20
    stock_threshold_sell = 80

    rsi_period = 14

    rsi_threshold_buy = 70
    rsi_threshold_sell = 30

    bandperiod = 20

    def init(self):
        self.macd, self.signal, self.hist = self.I(talib.MACD, self.data.Close, fastperiod=self.fastperiod, slowperiod=self.slowperiod, signalperiod=self.signalperiod)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.stoch_k, self.stoch_d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, fastk_period=self.fastk_period, slowk_period=self.slowk_period, slowd_period=self.slowd_period)
        self.upper, self.middle, self.lower = self.I(talib.BBANDS, self.data.Close, timeperiod=self.bandperiod, nbdevup=2, nbdevdn=2, matype=0)

    def next(self):
        if not np.isnan(self.hist) and not np.isnan(self.hist):
            if self.rsi < self.rsi_threshold_buy and self.stoch_k < self.stock_threshold_buy and self.data.Close < self.lower:
                self.buy()

            elif self.rsi > self.rsi_threshold_sell and self.stoch_k > self.stock_threshold_sell and self.data.Close > self.upper:
                self.sell()
class EMA_RSI_CCI_Strategy(Strategy):
    #def __init__(self):
    ema_short_period = 7
    ema_long_period = 21
    rsi_period = 21
    cci_period = 80
    cci_threshold_buy = 100
    cci_threshold_sell = 50

    def init(self):
        self.ema_short = self.I(talib.EMA, self.data.Close, self.ema_short_period)
        self.ema_long = self.I(talib.EMA, self.data.Close, self.ema_long_period)
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.cci = self.I(talib.CCI, self.data.High, self.data.Low, self.data.Close, self.cci_period)

    def next(self):
        if crossover(self.ema_short, self.ema_long) and self.rsi < 50 and self.cci > self.cci_threshold_buy:
            self.buy()
        elif crossover(self.ema_long, self.ema_short) and self.rsi > 50 and self.cci < self.cci_threshold_sell:
            self.sell()
class SmaCross(Strategy):
    n1 = 10
    n2 = 30

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
        self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2) and (self.rsi > 50):
            self.buy()
        elif crossover(self.sma2, self.sma1) and (self.rsi < 50):
            self.sell()
class MARibbonStrategy(Strategy):
    #mas = [5, 8, 13, 21, 34, 55]
    rsi_period = 20
    ma_5 = 7
    ma_21 = 24
    #macd_fast = 12
    #macd_slow = 26
    #macd_signal = 9
    #stoch_period = 14
    #stoch_k = 3
    #stoch_d = 3

    def init(self):
        # Compute moving averages the strategy demands
        #self.mas = [self.I(talib.SMA, self.data.Close, period) for period in self.mas]

        self.ema_5 = self.I(talib.EMA, self.data.Close, self.ma_5)
        self.ema_21 = self.I(talib.EMA, self.data.Close, self.ma_21)

        # Compute other indicators
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        #self.macd, self.macd_signal, _ = self.I(talib.MACD, self.data.Close, self.macd_fast, self.macd_slow, self.macd_signal)
        #self.stoch_k, self.stoch_d = self.I(talib.STOCH, self.data.High, self.data.Low, self.data.Close, self.stoch_period, self.stoch_k, self.stoch_d)

    def next(self):
        #if not self.position:
        #    if all(self.mas[i][-1] < self.mas[i + 1][-1] for i in range(len(self.mas) - 1)):
        #for i in range(len(self.mas)):
        #    print(self.mas[i][-1])
        #    print(self.mas[i][-4])
        #    #input()
        #if self.mas[1][-1] > self.mas[3][-1] and self.mas[1][-2] < self.mas[3][-2]:
        #if all(self.mas[1][-1] > self.mas[3][-1] and self.mas[1][-2] < self.mas[3][-2] for i in range(len(self.mas))):
        
        if crossover(self.ema_5, self.ema_21) and self.rsi < 50:
        #if all(self.mas[i][-1] > self.mas[i][-4] for i in range(len(self.mas))):
            #print('cross buy')
            #print(self.ema_5[-1])
            #print(self.ema_21[-1])
            #print(self.rsi[-1])
            #print(self.macd[-1])
            #print(self.macd_signal[-1])

            #if self.rsi < 30 and self.macd > self.macd_signal and self.stoch_k < 20:
            self.buy()
        #else:
        #if all(self.mas[i][-1] > self.mas[i + 1][-1] for i in range(len(self.mas) - 1)):
        #elif self.mas[1][-1] < self.mas[3][-1] and self.mas[1][-2] > self.mas[3][-2]:
        #elif all(self.mas[1][-1] < self.mas[3][-1] and self.mas[1][-2] > self.mas[3][-2] for i in range(len(self.mas))):
        elif crossover(self.ema_21, self.ema_5) and self.rsi > 50:
            #print('cross sell')
            #print(self.ema_5)
            #print(self.ema_21)
            #print(self.rsi)
            #print(self.macd)
            #print(self.macd_signal)
        #elif all(self.mas[i][-1] < self.mas[i][-4] for i in range(len(self.mas))):
            #if self.rsi > 70 and self.macd < self.macd_signal and self.stoch_k > 80:
            self.sell()

class ADXSMASStrategy(Strategy):
    #mas = [5, 8, 13, 21, 34, 55]
    adx_period = 25
    ma_9 = 9
    ma_26 = 26
    
    #stoch_d = 3

    def init(self):
        # Compute moving averages the strategy demands

        self.ema_9 = self.I(talib.EMA, self.data.Close, self.ma_9)
        self.ema_26 = self.I(talib.EMA, self.data.Close, self.ma_26)

        self.adx = self.I(talib.ADX, self.data.High,self.data.Low,self.data.Close, self.adx_period)

    def next(self):    
        if crossover(self.ema_9, self.ema_26) and self.adx < 25:
            self.buy()

        elif crossover(self.ema_26, self.ema_9) and self.adx > 25:
            self.sell()
#INSERT INTO `planes`(`id`, `agent`, `valor`, `network`, `lockt`, `tipo`, `fecha`, `hora`, `fechaco`, `horaco`, `estado`, `observ`) VALUES ('9870','162','210','TRC20USDT','24','Ganancia','2023-03-14','22:39:03','2023-03-14','22:39:03','ACTIVADO','Ninguna')
#zahir.ns.cloudflare.com
#lauryn.ns.cloudflare.com

class FibonacciStrategy(Strategy):
    #def __init__(self, buy_level=0.236, sell_level=0.618):
    buy_level = 0.236
    sell_level = 0.618
        
    def init(self):
        pass
    
    def next(self):
        highs = self.data.High
        lows = self.data.Low
        closes = self.data.Close
        
        # Calculate highest high and lowest low over the lookback period
        high_max = np.max(highs[:-1])
        low_min = np.min(lows[:-1])
        
        # Calculate Fibonacci levels
        diff = high_max - low_min
        levels = [low_min + self.buy_level * diff,
                  low_min + self.sell_level * diff]
        
        # Buy if price breaks above buy level
        if closes[-1] > levels[0]:
            self.buy()
        
        # Sell if price breaks below sell level
        elif closes[-1] < levels[1]:
            self.sell()
data = get_binance_data(symbol="APTUSDT", interval='15m', start_str='5 days ago UTC')
data.rename(columns={'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'})

print(data)
#bt = Backtest(data, EMA_RSI_CCI_Strategy, cash=1000, commission=.001, exclusive_orders=True)
bt = Backtest(data, MARibbonStrategy, cash=500, commission=.001, exclusive_orders=True)
#bt = Backtest(data, ADXSMASStrategy, cash=2000, commission=.001, exclusive_orders=True)
#optimización  maRibbon

stats =  bt.optimize(ma_5=range(5,9,1),ma_21=range(21,25,1),rsi_period =range(10,30,2))
#optimización  ADXsmas

#stats =  bt.optimize(ma_9=range(5,9,1),ma_26=range(21,26,1),adx_period =range(10,30,2))
#optimización  EmaRsiCci

#stats =  bt.optimize(ema_short_period=range(5,9,1),ema_long_period=range(21,25,1),rsi_period =range(10,30,2),cci_period=range(50,80,5),cci_threshold_buy=range(80,100,5),cci_threshold_sell=range(20,50,5))

#optimización  MACD



#stats =  bt.optimize(fastperiod=range(6,18,3),slowperiod=range(20,40,3),signalperiod =range(5,15,3),rsi_period =range(14,30,5),rsi_threshold_buy =range(50,70,5),rsi_threshold_sell =range(30,50,5))

# opt fibinacci


#stats = bt.run()
bt.plot()

print(stats)


 #14558 (155)
 #14561 (15)