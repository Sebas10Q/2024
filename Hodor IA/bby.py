import ccxt
import talib
import numpy as np
import datetime
import requests
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
# Initialize the exchange object
exchange = ccxt.bybit({
    'apiKey': '87CssLWM5vqDqLKF9v',
    'secret': 'IdUkAvTkBPKeC8b2Ih1nzgakGdO2ELHRKq44',
    'enableRateLimit': True,
    'rateLimit': 2000,
    'options': {'defaultType': 'future'}
})

# Define function to get recent OHLCV data
def get_recent_data(symbol, timeframe):
    #return exchange.fetch_ohlcv(symbol, timeframe)[-100:]
    current_datetime = datetime.datetime.now()

    # Set the start time to 12:00 AM (00:00:00) 7 days ago
    start_datetime = current_datetime - datetime.timedelta(days=1)
    #start_datetime = current_datetime - datetime.timedelta(minutes=5)
    start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    # Set the end time to the current date and time
    end_datetime = current_datetime

    # Convert the datetime objects to timestamps in milliseconds
    start_timestamp = int(start_datetime.timestamp() * 1000)
    end_timestamp = int(end_datetime.timestamp() * 1000)
    con = symbol.replace('/','')
    kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={con}&interval=15&start={start_timestamp}&end={end_timestamp}'
    kline_response = requests.get(kline_url)
    print(kline_url)
    kline_data = kline_response.json()
    data2 = np.array(kline_data['result']['list'])
    # Convert the elements to float and int values
    converted_data = np.array([[int(item) if item.isdigit() else float(item) for item in row] for row in data2])

    #print(converted_data)
    #print(data2[-100:])
    #dee = converted_data[-100:]
    #print(dee[:,4])
    return converted_data[-100:]

# Define function to calculate RSI
def calculate_rsi(data, rsi_period):
    rsi = talib.RSI(data[:, 4], timeperiod=rsi_period)
    return rsi

# Define function to detect hidden divergences
def detect_hidden_divergence(symbol, timeframe, rsi_period):
    # Get recent data for the symbol
    data = get_recent_data(symbol, timeframe)
    
    # Calculate RSI values
    rsi = calculate_rsi(data, rsi_period)

    

    # Calculate price swings
    highs = data[:, 2]
    lows = data[:, 3]
    
    price_swings = highs - lows

    
    # Detect hidden divergences
    hidden_divergences = []
    for i in range(1, len(data)):
        if rsi[i] > rsi[i - 1] and price_swings[i] > price_swings[i - 1]:
            #hidden_divergences.append("UP hidden divergence")
            hidden_divergences.append(1)
        elif rsi[i] < rsi[i - 1] and price_swings[i] < price_swings[i - 1]:
            #hidden_divergences.append("DOWN hidden divergence")
            hidden_divergences.append(-1)
        else:
            #hidden_divergences.append("No hidden divergence")
            hidden_divergences.append(0)
    
    return data, rsi, hidden_divergences

# Set the symbol, timeframe, and RSI period
symbol = 'OP/USDT'
timeframe = '1h'
rsi_period = 14

# Detect hidden divergences
#divergences = detect_hidden_divergence(symbol, timeframe, rsi_period)
#for i, divergence in enumerate(divergences, 1):
#    print(f"{i}. {divergence}")

# Detect hidden divergences and get data for plotting
data, rsi, divergences = detect_hidden_divergence(symbol, timeframe, rsi_period)

# Plot the price and RSI data
# plt.figure(figsize=(12, 6))
# plt.subplot(2, 1, 1)
# plt.plot(data[:, 0], data[:, 4], label='Price', color='blue')
# plt.title(f"{symbol} Price and RSI (Period: {rsi_period})")
# plt.ylabel("Price (USDT)")
# plt.grid(True)
# plt.legend()

# plt.subplot(2, 1, 2)
# plt.plot(data[:, 0], rsi, label='RSI', color='orange')
# plt.ylabel("RSI")
# plt.xlabel("Time")
# plt.grid(True)
# plt.legend()

# Create a DataFrame for the OHLCV data
df = pd.DataFrame(data[:, 1:5], columns=["Open", "High", "Low", "Close"], index=pd.to_datetime(data[:, 0], unit="ms"))
# Reverse the DataFrame to correct the order for plotting
df = df.iloc[::-1]

# Create a DataFrame for the RSI with datetime index
rsi_df = pd.DataFrame(rsi, columns=["RSI"], index=pd.to_datetime(data[:, 0], unit="ms"))

# Find the lowest points in price (price_swings_low)
price_swings_low = np.r_[True, data[1:, 4] < data[:-1, 4]] & np.r_[data[:-1, 4] < data[1:, 4], True]
# Find the highest points in price (price_swings_high)
price_swings_high = np.r_[True, data[1:, 4] > data[:-1, 4]] & np.r_[data[:-1, 4] > data[1:, 4], True]
# Find the lowest points in RSI (rsi_swings_low)
rsi_swings_low = np.r_[True, rsi[1:] < rsi[:-1]] & np.r_[rsi[:-1] < rsi[1:], True]

# Find the highest points in RSI (rsi_swings_high)
rsi_swings_high = np.r_[True, rsi[1:] > rsi[:-1]] & np.r_[rsi[:-1] > rsi[1:], True]

# Detect bullish hidden divergence
bullish_hidden_divergences = (price_swings_low[1:] & rsi_swings_high[:-1]).astype(int)

# Detect bearish hidden divergence
bearish_hidden_divergences = (price_swings_high[1:] & rsi_swings_low[:-1]).astype(int)

print(bullish_hidden_divergences)
print(bearish_hidden_divergences)
# Create a DataFrame for divergences with datetime index
# If divergences length is shorter than OHLCV data, remove the last timestamp from OHLCV data

if len(divergences) < len(df):
    df = df[:-1]
    rsi_df = rsi_df[:-1]
#divergences_df = pd.DataFrame(divergences, columns=["Divergence"], index=pd.to_datetime(data[:, 0], unit="ms"))
divergences_df = pd.DataFrame(divergences, columns=["Divergence"], index=pd.to_datetime(data[:len(divergences), 0], unit="ms"))
# Add the RSI as a subplot to the candlestick plot

apds = [mpf.make_addplot(rsi_df["RSI"], panel=1, color='orange', secondary_y=False),
        mpf.make_addplot(bullish_hidden_divergences, panel=2, color='green', scatter=True),
        mpf.make_addplot(bearish_hidden_divergences, panel=2, color='red', scatter=True)
        ]

# Plot the candlestick chart along with the RSI subplot
fig, axes = mpf.plot(df, type='candle', style='classic', title=f"{symbol} Price and RSI (Period: {rsi_period})", ylabel="Price (USDT)", volume=False, addplot=apds, returnfig=True)


# for i, divergence in enumerate(divergences_df["Divergence"]):
#     if divergence == "UP hidden divergence":
#         axes[0].scatter(data[i, 0], data[i, 4], color='green', marker='^', s=100)
#     elif divergence == "DOWN hidden divergence":
#         axes[0].scatter(data[i, 0], data[i, 4], color='red', marker='v', s=100)

plt.show()
# Create a new figure and subplots
# fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

# # Plot the price data as candles along with the RSI
# mpf.plot(df, type='candle', style='classic', title=f"{symbol} Price and RSI (Period: {rsi_period})", ylabel="Price (USDT)", volume=False, ax=axes[0])
# axes[0].grid(True)

# # Plot the RSI with datetime index
# axes[1].plot(rsi_df.index, rsi_df["RSI"], label='RSI', color='orange', alpha=0.7)
# axes[1].set_ylabel("RSI")
# axes[1].grid(True)
# Define the style of the candlestick plot
# mc = mpf.make_marketcolors(up='g', down='r')
# s  = mpf.make_mpf_style(marketcolors=mc)

# Plot the price data as candles along with the RSI
# mpf.plot(df, type='candle', style=s, title=f"{symbol} Price and RSI (Period: {rsi_period})", ylabel="Price (USDT)", volume=False)
# plt.plot(data[:, 0], rsi, label='RSI', color='orange', alpha=0.7)
# plt.ylabel("RSI")
# plt.grid(True)
# plt.legend()

# Plot the price data as candles along with the RSI
# mpf.plot(df, type='candle', style=s, title=f"{symbol} Price and RSI (Period: {rsi_period})", ylabel="Price (USDT)", volume=False)

# # Plot the RSI with datetime index
# plt.plot(rsi_df.index, rsi_df["RSI"], label='RSI', color='orange', alpha=0.7)
# plt.ylabel("RSI")
# plt.grid(True)
# plt.legend()
# Highlight the points where hidden divergences are detected
# for i, divergence in enumerate(divergences):
#     if divergence == "UP hidden divergence":
#         plt.scatter(data[i, 0], data[i, 4], color='green', marker='^', s=100)
#     elif divergence == "DOWN hidden divergence":
#         plt.scatter(data[i, 0], data[i, 4], color='red', marker='v', s=100)
# Highlight the points where hidden divergences are detected
# for i, divergence in enumerate(divergences):
#     if divergence == "UP hidden divergence":
#         axes[0].scatter(data[i, 0], data[i, 4], color='green', marker='^', s=100)
#     elif divergence == "DOWN hidden divergence":
#         axes[0].scatter(data[i, 0], data[i, 4], color='red', marker='v', s=100)
#plt.show()