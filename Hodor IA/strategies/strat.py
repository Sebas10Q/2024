from backtesting import Backtest, Strategy
from backtesting.test import SMA, GOOG
from backtesting.lib import crossover
import talib
import pandas as pd
import numpy as np



def newvwap(x,y,z,n):
    volume = n
    typical = ((x + y + z) / 3)
    vwap = np.cumsum(volume * typical) / np.cumsum(volume)
    return vwap


def MA_TA(df, n):
    # ma =df['Close'].rolling(window=n).mean()
    ma = talib.MA(df, n)
    return ma


def EMA(df, n):
    #ema_short = df.ewm(span=n, adjust=False).mean()
    ema_short = talib.EMA(df, n)
    return ema_short


def MDI(x, n):
    z = talib.MINUS_DI(x, x, x, n)
    return z


def PDI(x, n):
    z = talib.PLUS_DI(x, x, x, n)
    return z


def ADX(x, y, z, n):
    z = talib.ADX(x, y, z, n)
    return z


def EMAshort(x, n):
    EMA_short = talib.EMA(x, n)
    return EMA_short


def EMAMedium(x, n):
    EMA_medium = talib.EMA(x, n)
    return EMA_medium


def MACD(x, n_fast, n_slow):
    close = x['Close']
    macd = talib.MACD(x, n_fast, n_slow, 9)
    return macd


def MACDSign(x, n_fast, n_slow):
    macdsignal = talib.MACD(x, n_fast, n_slow, 9)
    return macdsignal


def MACDHist(x, n_fast, n_slow):
    macdhist = talib.MACD(x, n_fast, n_slow, 9)
    return macdhist


def SMAlong(x, n):
    SMA_long = talib.SMA(x, n)
    return SMA_long


def SMAshort(x, n):
    SMA_short = talib.SMA(x, n)
    return SMA_short


def SMAMedium(x, n):
    SMA_medium = talib.SMA(x, n)
    return SMA_medium


def SMA1(x, n):
    z = talib.SMA(x, n)
    return z


def MOM(x, n):
    z = talib.MOM(x, n)
    return z


def MINUS_DI(x,y,z, n):
    z = talib.MINUS_DI(x, y, z, n)
    return z


def PLUS_DI(x,y,z, n):
    z = talib.PLUS_DI(x, y, z, n)
    return z


def RSI(x, n):
    z = talib.RSI(x, n)
    return z

def clscalc(x):
    cls = (x).iloc[-1]
    return cls


def BBANDS(x, t, n, o, m):
    lowerband = talib.BBANDS(x, t, n, o, m).iloc[-1]
    return lowerband


def CCI(x, n):
    z = talib.CCI(x, x, x, n).iloc[-1]
    return z


def CCI1(x, n):
    CCI_ONE = talib.CCI(x, x, x, n).iloc[-1]
    return CCI_ONE


def CCI2(x, n):
    CCI_TWO = talib.CCI(x, x, x, n).iloc[-1]
    return CCI_TWO


def MFI(x, n):
    z = talib.MFI(x['High'], x['Low'], x['Close'], x['Volume'], n).iloc[-1]
    return z
    
def getADX(df):
    ADX = talib.ADX(df['High'],df['Low'],df['Close'], timeperiod=14).iloc[-1]
    return ADX

def getRSI(df):
    RSI = talib.RSI(df['Close'], timeperiod=14).iloc[-1]
    return RSI

def getSAR(df):
    SAR = talib.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2).iloc[-1]
    return SAR

class strat_ADX_SMAS(Strategy):
 
    def init(self):

        self.ADX = self.I(ADX,self.data.High,self.data.Low,self.data.Close,14)
        
   



    def next(self):
        if (self.ADX < 25):
            self.buy()
        elif (self.ADX > 25):
            self.sell()

class strat_SVARS(Strategy):
 
    def init(self):

        self.ADX = self.I(ADX,self.data.High,self.data.Low,self.data.Close,14)
        self.rsi = self.I(RSI, self.data.Close, 21)
        self.SAR = self.I(getSAR,self.data.High,self.data.Low,15)
        self.newvwap = self.I(newvwap,self.data.High,self.data.Low,self.data.Close,self.data.Volume)


    def next(self):
        if (self.newvwap > self.data.High[-1]) and (self.SAR < self.data.Close[-1]) and (self.rsi > 55) and (self.ADX > 24):
            self.buy()
        elif (self.newvwap < self.data.High[-1]) and (self.SAR > self.data.Close[-1]) and (self.rsi < 45) and (self.ADX > 24):
            self.sell()
            
class strat_ADX_MOMENTUM(Strategy):
 
    def init(self):

        self.ADX = self.I(ADX,self.data.High,self.data.Low,self.data.Close,14)
        self.MOM = self.I(MOM,self.data.Close,14)
        self.MINUS_DI = self.I(MINUS_DI,self.data.High,self.data.Low,self.data.Close,25)
        self.PLUS_DI = self.I(PLUS_DI,self.data.High,self.data.Low,self.data.Close,25)



    def next(self):
        if (self.ADX < 25) and (self.MOM > 0)  and (crossover(self.PLUS_DI,self.MINUS_DI)):
            self.buy()
        elif (self.ADX > 25) and (self.MOM < 0)  and (crossover(self.MINUS_DI,self.PLUS_DI)):
            self.sell()


class strat_BB_RSI(Strategy):
 
    def init(self):

        self.bbands = self.I(BBANDS, self.data.Close, 14)
        self.rsi = self.I(RSI, self.data.Close, 21)
        self.CLS = self.I(clscalc,self.data.Close)



    def next(self):
        if (self.rsi < 30) and (crossover(self.bbands,self.CLS)):
            self.buy()
        elif (self.rsi > 70):
            self.sell()



class strat_EMA_RSI_CCI(Strategy):
 
    def init(self):
    
        self.CCI = self.I(CCI,self.data.High,self.data.Low,self.data.Close,80)
        self.emamedium = self.I(EMAMedium, self.data.Close, 20)
        self.emashort = self.I(EMAshort, self.data.Close, 5)
        self.SMA1 = self.I(SMA1,self.data.Close,20)
        self.rsi = self.I(RSI, self.data.Close, 21)



    def next(self):
        if (crossover(self.emashort, self.emamedium)) and (self.rsi > 50) and (self.CCI > 50):
            self.buy()
        elif (crossover(self.emamedium, self.emashort)) and (self.rsi < 50) and (self.CCI < 50):
            self.sell()


class strat_BINDHAST(Strategy):
 
    def init(self):
        
        self.ADX = self.I(ADX,self.data.High,self.data.Low,self.data.Close,14)
        self.MA = self.I(MA_TA, self.data.Close, 10)
        self.EMA = self.I(EMA, self.data.Close, 5)


    def next(self):
        if (self.ADX > 25) and (crossover(self.EMA,self.MA)):
            self.buy()
        elif (self.ADX < 25) and (crossover(self.MA, self.EMA)):
            self.sell()

class strat_EMA_SMA_CLOSE(Strategy):
 
    def init(self):
        
        self.CLS = self.I(clscalc,self.data.Close)
        self.emamedium = self.I(EMAMedium, self.data.Close, 20)
        self.emashort = self.I(EMAshort, self.data.Close, 5)
        self.SMA1 = self.I(SMA1,self.data.Close,20)
        self.rsi = self.I(RSI, self.data.Close, 21)

    def next(self):
        if (crossover(self.emashort, self.emamedium)) and (crossover(self.CLS,self.SMA1)):
            self.buy()
        elif (crossover(self.emamedium, self.emashort)):
            self.sell()

class strat_EMA_RSI(Strategy):
 
    def init(self):
    
        self.emamedium = self.I(EMAMedium, self.data.Close, 50)
        self.emashort = self.I(EMAshort, self.data.Close, 7)
        self.rsi = self.I(RSI, self.data.Close, 21)



    def next(self):
        if (crossover(self.emamedium, self.emashort)) and (self.rsi > 50):
            self.buy()
        elif (crossover(self.emashort, self.emamedium))  and (self.rsi < 50):
            self.sell()
            
class SmaCross(Strategy):
    n1 = 10
    n2 = 30

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


