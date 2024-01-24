import pandas as pd
import numpy as np
import talib
import mysql.connector as mariadb

def MA_TA(df, n):
    #ma =df['Close'].rolling(window=n).mean()
    real = talib.MA(df['Close'], timeperiod=n, matype=0).iloc[-1]
    return real

def EMA(df,n):
    ema_short = df['Close'].ewm(span=n, adjust=False).mean().iloc[-1]
    return ema_short

def MDI(x, n):
    z = talib.MINUS_DI(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return z

def PDI(x, n):
    z = talib.PLUS_DI(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return z

def ADX(x, n):
    z = talib.ADX(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return z

def EMAshort(x, n):
    EMA_short = talib.EMA(x['Close'], n).iloc[-1]
    return EMA_short

def EMAMedium(x, n):
    EMA_medium = talib.EMA(x['Close'], n).iloc[-1]
    return EMA_medium

def MACD(x, n_fast, n_slow):
    close = x['Close']
    macd = talib.MACD(x['Close'], n_fast, n_slow, 9).iloc[-1]
    return macd

def MACDSign(x, n_fast, n_slow):
    macdsignal = talib.MACD(x['Close'], n_fast, n_slow, 9).iloc[-1]
    return macdsignal

def MACDHist(x, n_fast, n_slow):
    macdhist = talib.MACD(x['Close'], n_fast, n_slow, 9).iloc[-1]
    return macdhist

def SMAlong(x, n):
    SMA_long = talib.SMA(x['Close'], n).iloc[-1]
    return SMA_long

def SMAshort(x, n):
    SMA_short = talib.SMA(x['Close'], n).iloc[-1]
    return SMA_short
    
def SMAMedium(x, n):
    SMA_medium = talib.SMA(x['Close'], n).iloc[-1]
    return SMA_medium

def SMA(x, n):
    z = talib.SMA(x['Close'], n).iloc[-1]
    return z

def MOM(x, n):
    z = talib.MOM(x['Close'], n).iloc[-1]
    return z

def MINUS_DI(x, n):
    z = talib.MINUS_DI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return z

def PLUS_DI(x, n):
    z = talib.PLUS_DI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return z

def RSI(x, n):
    z = talib.RSI(x['Close'], n).iloc[-1]
    return z

def BBANDS(x, t, n, o, m):
    lowerband = talib.BBANDS(x['Close'], t, n, o, m).iloc[-1]
    return lowerband

def CCI(x, n):
    z = talib.CCI(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return z

def CCI1(x, n):
    CCI_ONE = talib.CCI(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return CCI_ONE

def CCI2(x, n):
    CCI_TWO = talib.CCI(x['High'],x['Low'],x['Close'], n).iloc[-1]
    return CCI_TWO

def MFI(x, n):
    z = talib.MFI(x['High'],x['Low'],x['Close'],x['Volume'], n).iloc[-1]
    return z
    
def newvwap(df):
    volume = float(df['Volume'].iloc[-1])
    sumn = float(df['High'].iloc[-1]) + float(df['Low'].iloc[-1]) + float(df['Close'].iloc[-1])
    typical = sumn / 3
    vwap = np.cumsum(volume * typical) / np.cumsum(volume)
    return vwap

def getADX(df):
    ADX = talib.ADX(df['High'],df['Low'],df['Close'], timeperiod=14).iloc[-1]
    return ADX

def getRSI(df):
    RSI = talib.RSI(df['Close'], timeperiod=14).iloc[-1]
    return RSI

def getSAR(df):
    SAR = talib.SAR(df['High'], df['Low'], acceleration=0.02, maximum=0.2).iloc[-1]
    return SAR

def strat_SVARS(df):
    VWAP = newvwap(df)
    ADX = getADX(df).iloc[-1]
    RSI = getRSI(df).iloc[-1]
    SAR = getSAR(df).iloc[-1]

    if (float(VWAP[0]) > float(df['High'].iloc[-1])) and (float(SAR) < float(df['Close'].iloc[-1])) and (float(RSI) > 55) and (float(ADX) > 24):
        return 'buy'
    elif (float(VWAP[0]) < float(df['High'].iloc[-1])) and (float(SAR) > float(df['Close'].iloc[-1])) and (float(RSI) < 45) and (float(ADX) > 24):
        return 'sell'

    return False


def strat_ADX_SMAS(df):
    #if (SMAlong(df.iloc[:-1,:], 26) > SMAshort(df.iloc[:-1,:], 9)) and (SMAlong(df, 26) < SMAshort(df, 9)):# and (ADX(df.iloc[:-1, :], 14) > 25)
    if (ADX(df, 14) < 25) :
        return 'buy'
    
    #elif (SMAlong(df.iloc[:-1, :], 26) < SMAshort(df.iloc[:-1, :], 9)) and (SMAlong(df, 26) > SMAshort(df, 9)) :#and
    elif (ADX(df, 14) > 25) :
        return 'sell'
    
    return False

def strat_ADX_MOMENTUM(df):
    if (ADX(df, 14) < 25) and (MOM(df, 14) > 0) and (MINUS_DI(df, 25) < 25) and (PLUS_DI(df.iloc[:-1, :], 25) < MINUS_DI(df.iloc[:-1, :], 25)) and (PLUS_DI(df, 25) > MINUS_DI(df, 25)):
        return 'buy'

    elif (ADX(df, 14) < 25) and (MOM(df, 14) < 0) and (MINUS_DI(df, 25) < 25)and (PLUS_DI(df.iloc[:-1, :], 25) > MINUS_DI(df.iloc[:-1, :], 25))  and (PLUS_DI(df, 25) < MINUS_DI(df, 25)):
        return 'sell'

    return False

def strat_BB_RSI(df):
    CLS = (df['Close']).iloc[-1]
    if (RSI(df, 14) < 30) and ((CLS(df) < BBANDS(df, 14))):
        return 'buy'

    elif (RSI(df, 14) > 70):
        return 'sell'

    return False

def strat_EMA_RSI_CCI(df):
    
    if (EMAMedium(df.iloc[:-1, :], 10) > EMAshort(df.iloc[:-1, :], 5)) and (EMAMedium(df, 10) < EMAshort(df, 5)) and (RSI(df, 21) > 50) and (CCI(df, 80) > 50):
        return 'buy'

    elif (EMAMedium(df.iloc[:-1, :], 10) < EMAshort(df.iloc[:-1, :], 5)) and (EMAMedium(df, 10) > EMAshort(df, 5)) and (RSI(df, 21) < 50) and (CCI(df, 80) < 50):
        return 'sell'

    return False

def strat_BINDHAST(df):
    if (ADX(df, 14) > 25) and ((MA_TA(df.iloc[:-1, :], 10) > EMA(df.iloc[:-1, :], 5)) and (MA_TA(df, 10) < EMA(df, 5))):
        return 'buy'

    elif (ADX(df, 14) < 25) and ((MA_TA(df.iloc[:-1, :], 10) < EMA(df.iloc[:-1, :], 5)) and (MA_TA(df, 10) > EMA(df, 5))):
        return 'sell'

    return False


def strat_EMA_SMA_CLOSE(df):
    CLS = (df['Close']).iloc[-1]
    if (float(EMAMedium(df.iloc[:-1, :], 20)) > float(EMAshort(df.iloc[:-1, :], 5))) and (float(EMAMedium(df, 20)) < float(EMAshort(df, 5))) and (float(CLS) > (float(SMA(df, 20)))):
        return 'buy'

    elif (EMAMedium(df.iloc[:-1, :], 20) < EMAshort(df.iloc[:-1, :], 5)) and (EMAMedium(df, 20) > EMAshort(df, 5)) :
        return 'sell'

    return False


def strat_EMA_RSI(df):
    print(EMAMedium(df, 20))
    if (EMAMedium(df.iloc[:-1, :], 20) > EMAshort(df.iloc[:-1, :], 5)) and (EMAMedium(df, 20) < EMAshort(df, 5)) and (RSI(df, 21) > 50):
        return 'buy'

    elif (EMAMedium(df.iloc[:-1, :], 20) < EMAshort(df.iloc[:-1, :], 5)) and (EMAMedium(df, 20) > EMAshort(df, 5)) and (RSI(df, 21) < 50):
        return 'sell'

    return False

#mariadb_connection = mariadb.connect(user='root', password='',
#                                     database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
#cursor1 = mariadb_connection.cursor()
#query = "SELECT Open,High,Low,Close,Volume,date FROM databtc LIMIT 365;"
#df = pd.read_sql_query(query, mariadb_connection)
#df['datetime'] = pd.to_datetime(df['date'])
#df = df.set_index('datetime')
#df.drop(['date'], axis=1, inplace=True)
#df.sort_values(by='datetime', inplace=True)


#print(df)

#maveg = MA_TA(df,200)
#emaveg = EMA(df,200)
#adxveg = ADX(df,20)

#print(adxveg)

#print(strat_EMA_RSI(df))
#print(strat_BINDHAST(df))
#print(strat_EMA_RSI_CCI(df))
#print(strat_BB_RSI(df))
#print(strat_ADX_MOMENTUM(df))
#print(strat_ADX_SMAS(df))

