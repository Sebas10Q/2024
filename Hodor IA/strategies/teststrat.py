import pandas as pd
import numpy as np
import talib
from binance.client import Client
import mysql.connector as mariadb
api_key = 'x7DDr5lM7AMxKPgS0hpw9faHsh18N3UFePHuSj7rQKXQoF0DqmzfIheYGSK2dRmr'
api_secret = 'I84PJAWizPwWcWRD0FsQ11KFLPOUq5evzq4543G1UvGTTcvHtqAZC0nmndK2PSqG'

client = Client(api_key,api_secret)


def MA_TA(df, n):
    # ma =df['Close'].rolling(window=n).mean()
    real = talib.MA(df['Close'], timeperiod=n, matype=0).iloc[-1]
    return real

def DMI(x, n):
    # Calculamos el DMI con TALIB
    dmi = talib.DX(x['High'], x['Low'], x['Close']).iloc[-1]

    print("DMI:", dmi)
    return dmi
def EMA(df, n):
    ema_short = df['Close'].ewm(span=n, adjust=False).mean().iloc[-1]
    return ema_short


def MDI(x, n):
    z = talib.MINUS_DI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return z


def PDI(x, n):
    z = talib.PLUS_DI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return z


def ADX(x, n):
    z = talib.ADX(x['High'], x['Low'], x['Close'], n).iloc[-1]
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


def BBANDS(x):
    #lowerband = talib.BBANDS(x['Close'], t, n, o, m).iloc[-1]
    upper, middle, lower = talib.BBANDS(x['Close'], timeperiod=17, nbdevup=1, nbdevdn=1, matype=0)



    return lower.iloc[-1]

def BBANDSUP(x):
    #lowerband = talib.BBANDS(x['Close'], t, n, o, m).iloc[-1]
    upper, middle, lower = talib.BBANDS(x['Close'], timeperiod=17, nbdevup=1, nbdevdn=1, matype=0)



    return upper.iloc[-1]


def CCI(x, n):
    z = talib.CCI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return z


def CCI1(x, n):
    CCI_ONE = talib.CCI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return CCI_ONE


def CCI2(x, n):
    CCI_TWO = talib.CCI(x['High'], x['Low'], x['Close'], n).iloc[-1]
    return CCI_TWO


def MFI(x, n):
    z = talib.MFI(x['High'], x['Low'], x['Close'], x['Volume'], n).iloc[-1]
    return z


def newvwap(df):
    volume = float(df['Volume'].iloc[-1])
    sumn = float(df['High'].iloc[-1]) + float(df['Low'].iloc[-1]) + float(df['Close'].iloc[-1])
    typical = sumn / 3
    vwap = np.cumsum(volume * typical) / np.cumsum(volume)
    return vwap


def getADX(df):
    ADX = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14).iloc[-1]
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

    if (float(VWAP[0]) > float(df['High'].iloc[-1])) and (float(SAR) < float(df['Close'].iloc[-1])) and (
            float(RSI) > 55) and (float(ADX) > 24):
        return 'buy'
    elif (float(VWAP[0]) < float(df['High'].iloc[-1])) and (float(SAR) > float(df['Close'].iloc[-1])) and (
            float(RSI) < 45) and (float(ADX) > 24):
        return 'sell'

    return "❌"


def strat_ADX_SMAS(df):
    # if (SMAlong(df.iloc[:-1,:], 26) > SMAshort(df.iloc[:-1,:], 9)) and (SMAlong(df, 26) < SMAshort(df, 9)):# and (ADX(df.iloc[:-1, :], 14) > 25)
    if (float(ADX(df, 14)) < 25) and (float(SMAlong(df.iloc[:-1,:], 26)) > float(SMAshort(df.iloc[:-1,:], 9))) and (float(SMAlong(df, 26)) < float(SMAshort(df, 9))):
        return '🟢 Compra'

    # elif (SMAlong(df.iloc[:-1, :], 26) < SMAshort(df.iloc[:-1, :], 9)) and (SMAlong(df, 26) > SMAshort(df, 9)) :#and
    elif (ADX(df, 14) > 25) and (SMAlong(df.iloc[:-1, :], 26) < SMAshort(df.iloc[:-1, :], 9)) and (SMAlong(df, 26) > SMAshort(df, 9)):
        return '🔴 Venta'

    return "❌"


def strat_ADX_MOMENTUM(df):

    if (float(ADX(df, 14)) < 25) and (float(MOM(df, 14)) > 0)  and (
            float(PLUS_DI(df.iloc[:-1, :], 25)) < float(MINUS_DI(df.iloc[:-1, :], 25))) and (float(PLUS_DI(df, 25)) > float(MINUS_DI(df, 25))):
        return '🟢 Compra'

    elif (float(ADX(df, 14)) < 25) and (float(MOM(df, 14)) < 0)  and (
            float(PLUS_DI(df.iloc[:-1, :], 25)) > float(MINUS_DI(df.iloc[:-1, :], 25))) and (float(PLUS_DI(df, 25)) < float(MINUS_DI(df, 25))):
        return '🔴 Venta'

    return "❌"


def strat_BB_RSI(df):

    CLS = (df['Close'].iloc[-1])

    #print('strat_BB_rsi')
    #print(float(CLS))
    #print(float(BBANDSUP(df)))
    #print(float(BBANDS(df)))
    #print(float(RSI(df, 14)))


    if (float(RSI(df, 14)) < 30) and (float(CLS) < float(BBANDS(df))):
        return '🟢 Compra'

    elif (float(RSI(df, 14)) > 70) and (float(CLS) > float(BBANDSUP(df))):
        return '🔴 Venta'

    return "❌"


def strat_EMA_RSI_CCI(df):

    #print('EMA_RSI_CCI')
    #print(float(CCI(df, 80)))
    #print(float(EMAMedium(df.iloc[:-1, :], 21)))
    #print(float(EMAshort(df.iloc[:-1, :], 7)))
    #print(float(EMAMedium(df, 21)))
    #print(float(EMAshort(df, 7)))


    if (float(EMAMedium(df.iloc[:-1, :], 21)) > float(EMAshort(df.iloc[:-1, :], 7))) and (float(EMAMedium(df, 21)) < float(EMAshort(df, 7))) and (
            float(RSI(df, 21)) > 50) and (float(CCI(df, 80)) > 100):
        return '🟢 Compra'

    elif (float(EMAMedium(df.iloc[:-1, :], 21)) < float(EMAshort(df.iloc[:-1, :], 7))) and (float(EMAMedium(df, 21)) > float(EMAshort(df, 7))) and (
            float(RSI(df, 21)) < 50) and (float(CCI(df, 80)) < 50):
        return '🔴 Venta'

    return "❌"


def strat_BINDHAST(df):

    #print('BindHast')
    #print(float(ADX(df, 14)))
    #print(float(MA_TA(df.iloc[:-1, :], 21)))
    #print(float(EMA(df.iloc[:-1, :], 7)))
    #print(float(MA_TA(df, 21)))
    #print(float(EMA(df, 7)))
    
    if (float(ADX(df, 14)) > 25) and (float(MA_TA(df.iloc[:-1, :], 21)) > float(EMA(df.iloc[:-1, :], 7))) and (float(MA_TA(df, 21)) < float(EMA(df, 7))):
        return '🟢 Compra'

    elif (float(ADX(df, 14)) < 25) and (float(MA_TA(df.iloc[:-1, :], 10)) < float(EMA(df.iloc[:-1, :], 5))) and (float(MA_TA(df, 10)) > float(EMA(df, 5))):
        return '🔴 Venta'

    return "❌"


def strat_EMA_SMA_CLOSE(df):
    CLS = (df['Close']).iloc[-1]
    if (float(EMAMedium(df.iloc[:-1, :], 20)) > float(EMAshort(df.iloc[:-1, :], 5))) and (
            float(EMAMedium(df, 20)) < float(EMAshort(df, 5))) and (float(CLS) > float(SMA(df, 20))):
        return '🟢 Compra'

    elif (float(EMAMedium(df.iloc[:-1, :], 20)) < float(EMAshort(df.iloc[:-1, :], 5))) and (float(EMAMedium(df, 20)) > float(EMAshort(df, 5))):
        return '🔴 Venta'

    return "❌"
def strat_DMI_RSI(df):

    #print('strat_ema_rsi')
    #print(float(EMAMedium(df.iloc[:-1, :], 21)))
    #print(float(EMAshort(df.iloc[:-1, :], 7)))
    #print(float(EMAMedium(df, 21)))
    print(float(DMI(df, 7)))

    if (float(PLUS_DI(df.iloc[:-1, :], 25)) < float(MINUS_DI(df.iloc[:-1, :], 25))) and (float(PLUS_DI(df, 25)) > float(MINUS_DI(df, 25))) and (
            float(RSI(df, 14)) < 30) and (float(ADX(df, 14)) < 23):
        return '🟢 Compra'

    elif (float(PLUS_DI(df.iloc[:-1, :], 25)) > float(MINUS_DI(df.iloc[:-1, :], 25))) and (float(PLUS_DI(df, 25)) < float(MINUS_DI(df, 25))) and (
            float(RSI(df, 14)) > 70) and (float(ADX(df, 14)) > 23):
        return '🔴 Venta'

    return "❌"

def strat_EMA_RSI(df):

    #print('strat_ema_rsi')
    #print(float(EMAMedium(df.iloc[:-1, :], 21)))
    #print(float(EMAshort(df.iloc[:-1, :], 7)))
    #print(float(EMAMedium(df, 21)))
    #print(float(EMAshort(df, 7)))

    if (float(EMAMedium(df.iloc[:-1, :], 21)) > float(EMAshort(df.iloc[:-1, :], 7))) and (float(EMAMedium(df, 21)) < float(EMAshort(df, 7))) and (
            float(RSI(df, 21)) > 50):
        return '🟢 Compra'

    elif (float(EMAMedium(df.iloc[:-1, :], 21)) < float(EMAshort(df.iloc[:-1, :], 7))) and (float(EMAMedium(df, 21)) > float(EMAshort(df, 7))) and (
            float(RSI(df, 21)) < 50):
        return '🔴 Venta'

    return "❌"
def tape_reading_strategy(df):
    # Calculate the RSI
    rsi = RSI(df['Close'], timeperiod=14)

    # Calculate the MACD
    macd, macdsignal, macdhist = MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Check for overbought or oversold conditions
    if rsi[-1] > 70:
        print('🔴 Overbought')
        if macd[-1] < macdsignal[-1]:
            return '🔴 Sell'

    if rsi[-1] < 30:
       
        print('🟢 Oversold')
        # Check for changes in trend
        if macd[-1] > macdsignal[-1]:
            return '🟢 Buy'

    

    return "❌"

def strat_MA_Ribbon(df):
    mas = [5, 8, 13, 21, 34, 55]
    mas_color = ['blue', 'red', 'green', 'purple', 'brown', 'orange']
    for i, ma in enumerate(mas):
        df[f'MA_{ma}'] = talib.SMA(df['Close'], timeperiod=ma)
    for i in range(len(mas) - 1):
        if df[f'MA_{mas[i]}'].iloc[-1] < df[f'MA_{mas[i+1]}'].iloc[-1]:
            return '🟢 Compra'
        elif df[f'MA_{mas[i]}'].iloc[-1] > df[f'MA_{mas[i+1]}'].iloc[-1]:
            return '🔴 Venta'
    return '❌'

def strat_fibonacci(df):
    fib_levels = talib.FIBONACCI(df['High'], df['Low'], df['Close'])
    if df['Close'].iloc[-1] > fib_levels[0]: # Buy if price breaks above 23.6% Fibonacci level
        return '🟢 Compra'
    elif df['Close'].iloc[-1] < fib_levels[2]: # Sell if price breaks below 61.8% Fibonacci level
        return '🔴 Venta'
    else:
        return '❌'
#def strat_macd(df):
#    macd, signal, hist = talib.MACD(df['Close'])#Z

#    if hist[-2] < 0 and hist[-1] > 0: # Buy signal if MACD histogram crosses above zero
#        return '🟢 Compra'
#    elif hist[-2] > 0 and hist[-1] < 0: # Sell signal if MACD histogram crosses below zero
#        return '🔴 Venta'
#    else:
#        return '❌'
def strat_macd(df):
    # Calculate MACD
    macd, signal, hist = talib.MACD(df['Close'])

    print(hist)
    
    # Calculate RSI
    rsi = talib.RSI(df['Close'])
    
    # Calculate Stochastic Oscillator
    slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Close'])
    
    # Calculate Bollinger Bands
    upper, middle, lower = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    
    # Convert pandas Series to NumPy arrays or Python lists
    hist_array = hist.to_numpy()
    rsi_array = rsi.to_numpy()
    slowk_array = slowk.to_numpy()
    close_array = df['Close'].to_numpy()
    lower_array = lower.to_numpy()
    upper_array = upper.to_numpy()
    
    # Check for buy signal
    if not np.isnan(hist_array[-2]) and not np.isnan(hist_array[-1]):
        if hist_array[-2] < 0 and hist_array[-1] > 0 and rsi_array[-1] < 30 and slowk_array[-1] < 20 and close_array[-1] < lower_array[-1]:
            return '🟢 Compra'
    
        # Check for sell signal
        elif hist_array[-2] > 0 and hist_array[-1] < 0 and rsi_array[-1] > 70 and slowk_array[-1] > 80 and close_array[-1] > upper_array[-1]:
            return '🔴 Venta'
    
    return '❌'
def strat_pivot_points(df):
    pivot_levels = talib.PIVOT(df['High'], df['Low'], df['Close'])
    if df['Close'].iloc[-1] > pivot_levels[1]: # Buy if price breaks above R1 level
        return '🟢 Compra'
    elif df['Close'].iloc[-1] < pivot_levels[2]: # Sell if price breaks below S1 level
        return '🔴 Venta'
    else:
        return '❌'

def key_level_strategy(df, level=0.5):
    # Calculate moving average
    ma = talib.MA(df['close'], timeperiod=20, matype=0)
    
    # Calculate difference between current price and moving average
    diff = df['close'] - ma
    
    # Check if conditions for buying or selling are met
    if (diff[-1] > level) and (diff[-2] <= level):
        return '🟢 Compra'
    elif (diff[-1] < -level) and (diff[-2] >= -level):
        return '🔴 Venta'
    else:
        return '❌'

def dmi_adx_strategy(df):
    # Calculate DMI and ADX indicators
    plus_di = talib.PLUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
    minus_di = talib.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
    adx = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    
    # Check if conditions for buying or selling are met
    if (plus_di[-2] < minus_di[-2]) and (plus_di[-1] > minus_di[-1]) and (talib.RSI(df['close'], timeperiod=14)[-1] < 30) and (adx[-1] < 23):
        return '🟢 Compra'
    elif (plus_di[-2] > minus_di[-2]) and (plus_di[-1] < minus_di[-1]) and (talib.RSI(df['close'], timeperiod=14)[-1] > 70) and (adx[-1] > 23):
        return '🔴 Venta'
    else:
        return '❌'

def dmi_adx_key_level_strategy(df):
    if float(PLUS_DI(df.iloc[:-1, :], 25)) < float(MINUS_DI(df.iloc[:-1, :], 25)) and float(PLUS_DI(df, 25)) > float(MINUS_DI(df, 25)) and \
        float(RSI(df, 14)) < 30 and float(ADX(df, 14)) < 23 and float(EMAMedium(df, 21)) > float(EMAshort(df, 7)) and \
        df.iloc[-1]['Close'] > float(key_level_strategy(df)):
        return '🟢 Compra'
    
    elif float(PLUS_DI(df.iloc[:-1, :], 25)) > float(MINUS_DI(df.iloc[:-1, :], 25)) and float(PLUS_DI(df, 25)) < float(MINUS_DI(df, 25)) and \
        float(RSI(df, 14)) > 70 and float(ADX(df, 14)) > 23 and float(EMAMedium(df, 21)) < float(EMAshort(df, 7)) and \
        df.iloc[-1]['Close'] < float(key_level_strategy(df)):
        return '🔴 Venta'
        
    return "❌"
# mariadb_connection = mariadb.connect(user='root', password='',
#                                     database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
# cursor1 = mariadb_connection.cursor()
# query = "SELECT Open,High,Low,Close,Volume,date FROM databtc LIMIT 365;"
# df = pd.read_sql_query(query, mariadb_connection)
# df['datetime'] = pd.to_datetime(df['date'])
# df = df.set_index('datetime')
# df.drop(['date'], axis=1, inplace=True)
# df.sort_values(by='datetime', inplace=True)

#df = client.get_historical_klines(symbol="BNBUSDT", interval= '4h', start_str= '17 days ago UTC')
#
#
#
#df2 = pd.DataFrame(df,  columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
# #print(df2)
# # maveg = MA_TA(df,200)
# # emaveg = EMA(df,200)
# # adxveg = ADX(df,20)
#
# # print(adxveg)
# print(BBANDS(df2))
# print(strat_EMA_RSI(df2))
# print(strat_BINDHAST(df2))
# print(strat_EMA_RSI_CCI(df2))
# print(strat_BB_RSI(df2))
# print(strat_ADX_MOMENTUM(df2))
#print(strat_macd(df2))