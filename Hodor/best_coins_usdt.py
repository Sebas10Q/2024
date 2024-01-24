import datetime
from time import sleep
from time import gmtime, strftime
from datetime import timedelta
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
import requests
import os
from string import Template
import mysql.connector as mariadb
#from algotrade import telegram_bot_sendtext


##API key:
##
##
##API secret key:
##
##6SiwdIV0ye4baDzQBN6FsrpJwSaE0VZK8bqiJcy1FRLoLtmmze
##
##
##Access token :
##1017820859464060928-pXeDpn7JVtJm4WYX5jo6qoyzM8YTdp
##Access token secret :
##vvz3PeOrtV38rcmmD6xSxYsf5WMbJwvOFWFbPE8uFklTI
import twitter
api = twitter.Api(consumer_key='B0U43TCjBJg5SsAqm7C6jyY3N',
                      consumer_secret='9SRPpFoy66vIB1Lxml8fOB7uCfY90kyRTREkqVbchOfuoeGRaj',
                      access_token_key='1017820859464060928-J1vqtTozDMNYszihNfGAPPwS0CJBUP',
                      access_token_secret='I4BpTaf3uSU6iONujdIpRlVrbfRAudmydJLCIruz1lMYn')

api_key = 'x7DDr5lM7AMxKPgS0hpw9faHsh18N3UFePHuSj7rQKXQoF0DqmzfIheYGSK2dRmr'
api_secret = 'I84PJAWizPwWcWRD0FsQ11KFLPOUq5evzq4543G1UvGTTcvHtqAZC0nmndK2PSqG' 

client = Client(api_key,api_secret)

def telegram_bot_sendtext(bot_message,bot_message2):
    
    bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
    #bot_chatID = '-1101441080121'
    mariadb_connection = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                         database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
    cursor1 = mariadb_connection.cursor()
    query = "SELECT chatid, type FROM users;"
    df  = pd.read_sql_query(query,mariadb_connection)
    countid = 0
    bot_token2 = "1702282920:AAHhmp36xRntrPIF-HAEuHdLrufQ8QbwinI"
    bot_chatIDch1 = "-1001161788826"
    #"--549633523" chat señales
    send_text = 'https://api.telegram.org/bot' + bot_token2 + '/sendMessage?chat_id=' + bot_chatIDch1 + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    print(response.json())

    for x in range(len(df)):

        #print(df['chatid'][countid])
        usertype = df['type'][countid]
        if usertype == "free":
            bot_chatID = str(df['chatid'][countid])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
            response = requests.get(send_text)
            print(response.json())
        if usertype == "prem":
            bot_chatID = str(df['chatid'][countid])
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message2
            response = requests.get(send_text)
            print(response.json())
        #return response.json()
        countid = countid + 1
        
if __name__ == "__main__":
    while True:
        d2 = datetime.datetime.now()
        # for attr in [ 'hour', 'minute', 'second']:
        #	print attr, ':', getattr(d, attr)

        hoursact2 = getattr(d2, 'hour')
        minutesact2 = getattr(d2, 'minute')
        secondsact2 = getattr(d2, 'second')

        timeactual2 = timedelta(hours=hoursact2, minutes=minutesact2, seconds=secondsact2)
        timeactualdelta2 = pd.Timedelta(timeactual2)
        timeactualseconds2 = timeactualdelta2.total_seconds()

        print("Tiempo inicial: {}".format(timeactualseconds2))

        #r = requests.get('https://www.binance.com/exchange-api/v1/public/asset-service/product/get-products')
        #print(r)
        #r = 'https://api.bybit.com/v2/public/symbols'
        #r = 'https://api.bybit.com/spot/v3/public/symbols'
        r = 'https://api.bybit.com/derivatives/v3/public/instruments-info'
        response = requests.get(r)
        data = response.json()
        #print(data)
        crypto_df = pd.DataFrame(data['result']['list'])
        #print(crypto_df)
        usdt_symbols = crypto_df[crypto_df['quoteCoin'] == 'USDT']
        #cryptos = r.json()
        #cryptos= client.get_products()
        #print(cryptos['data'])
        #crypto_df= pd.DataFrame(cryptos['data'])
        #crypto_df= crypto_df[['b', 'an', 'q', 's']]
        #crypto_df.set_index('s')

        #crypto_df= crypto_df[crypto_df['q'] == 'USDT']


        dict_cryptos2 = {}
        for i, row in usdt_symbols.iterrows():
            symbol = row['symbol']
            #print(symbol)
            #kline_url = f'https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval=4h'
            # Get the current date and time
            current_datetime = datetime.datetime.now()

            # Set the start time to 12:00 AM (00:00:00) 7 days ago
            start_datetime = current_datetime - datetime.timedelta(days=1)
            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

            # Set the end time to the current date and time
            end_datetime = current_datetime

            # Convert the datetime objects to timestamps in milliseconds
            start_timestamp = int(start_datetime.timestamp() * 1000)
            end_timestamp = int(end_datetime.timestamp() * 1000)
            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval=60&limit=100&start={start_timestamp}&end={end_timestamp}'
            #kline_url = f'https://api.bybit.com/spot/v3/public/quote/kline?symbol={symbol}&interval=4h&limit=100'
            kline_response = requests.get(kline_url)
            kline_data = kline_response.json()
            #print(kline_data['result']['list'])
            dict_cryptos2[symbol] = pd.DataFrame(kline_data['result']['list'])

        sharpe_dict2 = {}
        for symbol, df in dict_cryptos2.items():
            
            df['Open time'] = pd.to_datetime(df[0], unit='ms')
            df.set_index('Open time', inplace=True)
            #df['Close'] = df['c'].astype(float)
            df['Close'] = pd.to_numeric(df[4])
            df['Norm'] = df['Close'] / df['Close'].iloc[0]
            #print(df['Norm'])
            df['Daily Return'] = df['Norm'].pct_change(1)

            
            df['Daily Return'].dropna(inplace=True)
            sharpe_dict2[symbol] = df['Daily Return'].mean() / df['Daily Return'].std() * (252 ** 0.5)
        # # Create an empty dictionary to store the processed data
        # dict_cryptos = {}

        # # Process the data for each symbol
        # for item in data:
        #     symbol = item['s']  # Get the symbol name
        #     df = pd.DataFrame([item])  # Create a DataFrame from the dictionary
        #     df['Open time'] = pd.to_datetime(df['t'], unit='ms')  # Convert the timestamp to datetime
        #     df.set_index('Open time', inplace=True)  # Set the Open time as the index
        #     df['Close'] = pd.to_numeric(df['c'])  # Convert the Close column to numeric values
        #     df['Norm'] = df['Close'] / df['Close'].iloc[0]  # Calculate the normalized values
        #     df['Daily Return'] = df['Norm'].pct_change(1)  # Calculate the daily returns
        #     df['Daily Return'].dropna(inplace=True)  # Drop any rows with missing values
        #     sharpe_dict[symbol] = df['Daily Return'].mean() / df['Daily Return'].std() * (252 ** 0.5)  # Calculate the Sharpe Ratio

        sharpe_sr2 = pd.Series(sharpe_dict2)

        best = sharpe_sr2.nlargest(10)
        print(best)
        best2 = sharpe_sr2.nlargest(25)
        best3 = sharpe_sr2.nsmallest(25)
        print(best3)

        usdt_symbols.set_index('symbol')
        
#         dict_cryptos={}
#         for i in range(len(usdt_symbols.name)):
                
#                 #print(crypto_df.s.values[i])
#                 try:
#                     dict_cryptos[usdt_symbols.name.values[i]] = client.get_historical_klines(symbol=usdt_symbols.alias.values[i],
#                                                                                        interval='4h',
#                                                                                        start_str='5 days ago UTC')
#                 except BinanceAPIException as e:
#                     print (e.status_code)
#                     print (e.message)


#                 #if crypto_df.s.values[i] != "MATICBTC" and crypto_df.s.values[i] != "ATOMBTC" and crypto_df.s.values[i] != "PHBBTC" and crypto_df.s.values[i] != "ONEBTC" and crypto_df.s.values[i] != "ALGOBTC" and crypto_df.s.values[i] != "ERDBTC" and crypto_df.s.values[i] != "WINBTC" and crypto_df.s.values[i] != "COSBTC" and crypto_df.s.values[i] != "TOMOBTC" and crypto_df.s.values[i] != "BANDBTC" and crypto_df.s.values[i] != "XTZBTC" and crypto_df.s.values[i] != "PNTBTC" and crypto_df.s.values[i] != "DGBBTC" and crypto_df.s.values[i] != "DAIBTC" and crypto_df.s.values[i] != "MKRBTC" and crypto_df.s.values[i] != "UMABTC":
#                 #        dict_cryptos[crypto_df.b.values[i]]= client.get_historical_klines(symbol=crypto_df.s.values[i], interval= '4h', start_str= '17 days ago UTC')
#                 sleep(0.1)
# ##Sharpe Ratio
#         sharpe_dict={}
#         for i in range(len(dict_cryptos)):
#                 print(list(dict_cryptos.keys())[i])
#                 try:
#                     if list(dict_cryptos.keys())[i] != "HNTUSDT" and list(dict_cryptos.keys())[i] != "SRMUSDT":
#                         vars() [list(dict_cryptos.keys())[i]]= pd.DataFrame(list(dict_cryptos.values())[i],  columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
#                         vars() [list(dict_cryptos.keys())[i]]['Open time']= pd.to_datetime(vars() [list(dict_cryptos.keys())[i]]['Open time'], unit='ms')
#                         vars() [list(dict_cryptos.keys())[i]].set_index('Open time',inplace=True)
#                         vars() [list(dict_cryptos.keys())[i]]['Close']= vars() [list(dict_cryptos.keys())[i]]['Close'].astype(float, copy=False)
#                         vars() [list(dict_cryptos.keys())[i]]['Norm']= vars() [list(dict_cryptos.keys())[i]]['Close']/vars() [list(dict_cryptos.keys())[i]]['Close'][0]
#                         vars() [list(dict_cryptos.keys())[i]]['Daily Return']= vars() [list(dict_cryptos.keys())[i]]['Norm'].pct_change(1)
#                         vars() [list(dict_cryptos.keys())[i]]['Daily Return'].dropna(inplace=True)
#                         sharpe_dict[list(dict_cryptos.keys())[i]]= vars() [list(dict_cryptos.keys())[i]]['Daily Return'].mean()/vars() [list(dict_cryptos.keys())[i]]['Daily Return'].std()*(252**0.5)
#                 except:
#                      pass
#         sharpe_sr= pd.Series(sharpe_dict)

#         best = sharpe_sr.nlargest(10)
#         print(best)
#         best2 = sharpe_sr.nlargest(25)
#         best3 = sharpe_sr.nsmallest(25)

        #Actualizar BD
        
        mariadb_connection = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                             database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
        cursor = mariadb_connection.cursor()
        col1 = best.index
        count1 = 0
        for valor2 in best:
                
                count1 = count1 + 1
                cursor.execute("""UPDATE topcoinsu SET porcentaje = %s WHERE coin_id = %s""",(valor2,count1))
                mariadb_connection.commit()


        count = 0
        
        for valor in col1:
                
                count = count + 1
                cursor.execute("""UPDATE topcoinsu SET coin_name = %s WHERE coin_id = %s""",(valor,count))
                mariadb_connection.commit()
                
        col2 = best2.index
        count3 = 0
        for valor3 in best2:
                
                count3 = count3 + 1

                cursor.execute("""UPDATE top25coinsu SET porcentaje = %s WHERE coin_id = %s""",(valor3,count3))
                mariadb_connection.commit()


        count4 = 0
        
        for valor4 in col2:
                
                count4 = count4 + 1
                cursor.execute("""UPDATE top25coinsu  SET coin_name = %s WHERE coin_id = %s""",(valor4,count4))
                mariadb_connection.commit()

        count5 = 0
        for valor5 in best2:
            count5 = count5 + 1
            cursor.execute("""UPDATE top_25_coins_newu SET porcomp = %s WHERE coin_id = %s""", (valor5, count5))
            mariadb_connection.commit()

        count6 = 0

        for valor6 in col2:
            count6 = count6 + 1
            cursor.execute("""UPDATE top_25_coins_newu  SET coin_name = %s WHERE coin_id = %s""", (valor6, count6))
            mariadb_connection.commit()
        col3 = best3.index
        count7 = 0
        for valor7 in best3:
            count7 = count7 + 1

            cursor.execute("""UPDATE top25coinspu SET porcentaje = %s WHERE coin_id = %s""", (valor7, count7))
            mariadb_connection.commit()

        count8 = 0

        for valor8 in col3:
            count8 = count8 + 1
            cursor.execute("""UPDATE top25coinspu  SET coin_name = %s WHERE coin_id = %s""", (valor8, count8))
            mariadb_connection.commit()
        
        #Seleccionar tiempo actualizado
        query = "SELECT twitter_time FROM topcoinsu;"
        df  = pd.read_sql_query(query,mariadb_connection)
        d1 = pd.DataFrame(df)
        time1 =d1['twitter_time'][0]
        time2 = pd.to_timedelta(time1)
        
        #Tiempo seleccionado + 1 hs
        time3 = pd.Timedelta(time2)
        time4 = time3.total_seconds()
        #print ('hora actualizaci0n:',(time4))
        hoursd = (time4 // 3600) + 1				
        minutesd = (time4 % 3600) // 60
        secondsd = time4 % 60
        timeact = timedelta(hours=hoursd,minutes=minutesd,seconds=secondsd)
        timeactdelta = pd.Timedelta(timeact)
        timeactseconds = timeactdelta.total_seconds()
        
        #print ('hora Nueva:',(timeactseconds))
        
        
        #Tiempo actual a comparar
        
        d = datetime.datetime.now()
        #for attr in [ 'hour', 'minute', 'second']:
        #	print attr, ':', getattr(d, attr)
        
        hoursact = getattr(d, 'hour')
        minutesact = getattr(d, 'minute')
        secondsact = getattr(d, 'second')
        
        timeactual = timedelta(hours=hoursact,minutes=minutesact,seconds=secondsact)
        timeactualdelta = pd.Timedelta(timeactual)
        timeactualseconds = timeactualdelta.total_seconds()
        symm = ["📈", "📈", "📈", "📈", "📈", "📈", "📈", "📈", "📈", "📈"]
        green = ["🟢", "🟢", "🟢", "🟢", "🟢", "🟢", "🟢", "🟢", "🟢", "🟢"]

        print ('hora actual:',(timeactualseconds))
        frame = {'Ret': best, '%': symm}

        result = pd.DataFrame(frame)
        #print(result)
        if (timeactualseconds <= timeactseconds) and (timeactualseconds >= time4):
                print('Estamos recopilando datos \n Wait please \n wait please')

                #best[1] = "d"

                #best["Added values"] = best[0].add(list)
                print(best.index)


        
        else:
                print('Actualizando twitter')
                #send_twit = best.to_string()
                s = Template('🔝 #Crypto 🔝 \n #Crypto \n $what \n Mas informacion #crypto http://t.me/labusiness_Bot')
                send_twit = s.substitute(what=result.iloc[0:5].to_string())
                s2 = Template('🔝 Crypto 🔝 \n Revisa nuestros planes de inversion https://hodorinvestments.com/plans/ \n $what')
                send_twit2 = s2.substitute(what=result.iloc[0:5].to_string())
                send_twit3 = s2.substitute(what=result.to_string())                
                #status = api.PostUpdate(send_twit)
                telegram_bot_sendtext(send_twit2,send_twit3)

                #Tiempo actualizar
                valor3 = strftime("%H:%M:%S", gmtime())
                count3 = 1
                cursor.execute("""UPDATE topcoinsu SET twitter_time = %s WHERE coin_id = %s""",(timeactual,count3))
                mariadb_connection.commit()
        mariadb_connection.close()
        break