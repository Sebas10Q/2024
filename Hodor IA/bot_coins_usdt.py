import datetime
import itertools
import os
from binance.exceptions import BinanceAPIException
import time
import subprocess
import prettytable
from strategies.stratalts2 import strat_DMI_RSI, strat_SVARS, strat_EMA_RSI, strat_EMA_SMA_CLOSE, strat_BINDHAST, strat_EMA_RSI_CCI, strat_BB_RSI, strat_ADX_MOMENTUM, strat_ADX_SMAS, strat_MA_Ribbon, dmi_adx_key_level_strategy, strat_macd
import requests
from time import sleep
from time import gmtime, strftime
from datetime import timedelta
from binance.client import Client
import pandas as pd
from string import Template
import mysql.connector as mariadb
import twitter
import pytz
import tabulate


api = twitter.Api(consumer_key='QJ9CyPJ1W2lvfKvRn88COS7SS',
                      consumer_secret='6SiwdIV0ye4baDzQBN6FsrpJwSaE0VZK8bqiJcy1FRLoLtmmze',
                      access_token_key='1017820859464060928-pXeDpn7JVtJm4WYX5jo6qoyzM8YTdp',
                      access_token_secret='vvz3PeOrtV38rcmmD6xSxYsf5WMbJwvOFWFbPE8uFklTI')

api2 = twitter.Api(consumer_key='S0UcePrq9KsH1th3YXr5ivC5r',
                      consumer_secret='oqyODjJx39ZK4A4lfXhHvGXjz8tr4eTNALdGU3YcAOGey0VDjJ',
                      access_token_key='1393731916990402563-KXElxRmWywntMRQ3UsEhEdmrRjiEF9',
                      access_token_secret='D9aJJRVlNyGQ9PKwMEdBawJBHaqDFFOAaa8hPtrlrfHyr')
api_key = 'dbBHY6nYFq5iAICvRwqHzaubTiCb8zk5aA11YR0inwsyKr4Tt7XqM46hjCcQoN0k'
api_secret = 'yJVvtuRF52Ldkl0nLSNfKhfczv087KPLWMKqfcAfRfWsbGntssCeacc07nYfVsGv'

client = Client(api_key, api_secret)


def telegram_bot_sendtext(listpro,listpro2):
    bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
    # bot_chatID = '-1101441080121'
    mariadb_connection = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                         database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
    cursor1 = mariadb_connection.cursor()
    query = "SELECT chatid, type FROM users;"
    df = pd.read_sql_query(query, mariadb_connection)
    countid = 0

    listmov = pd.DataFrame(listpro2)

    if len(listmov.index) > 0:
        for index, sigdata in pd.DataFrame(listpro2).iloc[0:4, 0:4].iterrows():
            IST = pytz.timezone('America/Bogota')
            e = datetime.datetime.now(IST)

            hours = getattr(e, 'hour')
            minutes = getattr(e, 'minute')
            second = getattr(e, 'second')
            days = getattr(e, 'day')
            month = getattr(e, 'month')
            year = getattr(e, 'year')

            dateup = str(year) + "-" + str(month) + "-" + str(days)
            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                sigdata['Coin'], dateup)
            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
            verify = False

            if len(dfsigver) > 0:
                hour = dfsigver['hour'].iloc[-1]
                print('Hora pedido:', (hour))
                time2 = pd.to_timedelta(hour)

                # Tiempo seleccionado + 1 hs
                time3 = pd.Timedelta(time2)
                time4 = time3.total_seconds()
                print('hora actualizaci0n:', (time4))
                hoursd = (time4 // 3600) + 4
                minutesd = (time4 % 3600) // 60
                secondsd = time4 % 60
                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                timeactdelta = pd.Timedelta(timeact)
                timeactseconds = timeactdelta.total_seconds()

                print('Hora vencimiento:', (timeactseconds))
                d = datetime.datetime.now()

                IST = pytz.timezone('America/Bogota')
                e = datetime.datetime.now(IST)
                print(e)

                hoursact = getattr(e, 'hour')
                minutesact = getattr(e, 'minute')
                secondsact = getattr(e, 'second')

                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                timeactualdelta = pd.Timedelta(timeactual)
                timeactualseconds = timeactualdelta.total_seconds()
                if timeactualseconds >= timeactseconds:
                    verify = True
                else:
                    verify = False
            if verify == True:
                bot_message = "₿ Par" + sigdata['Coin'] + '⚠⚠\n ➕ BBRSI {} \n ➕ EMARSI {} \n ➕ BINDHAST{} '.format(
                    sigdata['BBRSI'], sigdata['EMARSI'], sigdata['BINDHAST'])

                s = Template('🔝 Analisis 🔝 \n #Binance \n $what \n Info #crypto https://t.me/labusiness_Bot')
                send_twit = s.substitute(what=bot_message)
                bot_token2 = "1702282920:AAHhmp36xRntrPIF-HAEuHdLrufQ8QbwinI"
                bot_chatIDch1 = "-1001161788826"
                # "--549633523" chat señales
                send_text = 'https://api.telegram.org/bot' + bot_token2 + '/sendMessage?chat_id=' + bot_chatIDch1 + '&parse_mode=Markdown&text=' + bot_message
                response = requests.get(send_text)
                print(response.json())
                # try:
                #     status = api.PostUpdate(send_twit)
                #     status2 = api2.PostUpdate(send_twit)
                # except:
                #     pass
    for x in range(len(df)):

        usertype = df['type'][countid]

        if usertype == "free":
            listmov2 = pd.DataFrame(listpro2)

            if len(listmov2.index) > 0:
                for index, sigdata in pd.DataFrame(listpro2).iloc[0:4, 0:4].iterrows():
                    IST = pytz.timezone('America/Bogota')
                    e = datetime.datetime.now(IST)

                    hours = getattr(e, 'hour')
                    minutes = getattr(e, 'minute')
                    second = getattr(e, 'second')
                    days = getattr(e, 'day')
                    month = getattr(e, 'month')
                    year = getattr(e, 'year')

                    dateup = str(year) + "-" + str(month) + "-" + str(days)
                    hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                    query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                        sigdata['Coin'], dateup)
                    dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                    verify = False

                    if len(dfsigver) > 0:
                        hour = dfsigver['hour'].iloc[-1]
                        print('Hora pedido:', (hour))
                        time2 = pd.to_timedelta(hour)

                        # Tiempo seleccionado + 1 hs
                        time3 = pd.Timedelta(time2)
                        time4 = time3.total_seconds()
                        print('hora actualizaci0n:', (time4))
                        hoursd = (time4 // 3600) + 4
                        minutesd = (time4 % 3600) // 60
                        secondsd = time4 % 60
                        timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                        timeactdelta = pd.Timedelta(timeact)
                        timeactseconds = timeactdelta.total_seconds()

                        print('Hora vencimiento:', (timeactseconds))
                        d = datetime.datetime.now()

                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)
                        print(e)

                        hoursact = getattr(e, 'hour')
                        minutesact = getattr(e, 'minute')
                        secondsact = getattr(e, 'second')

                        timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                        timeactualdelta = pd.Timedelta(timeactual)
                        timeactualseconds = timeactualdelta.total_seconds()
                        if timeactualseconds >= timeactseconds:
                            verify = True
                        else:
                            verify = False
                    if verify == True:
                        print(sigdata['Coin'])
                        bot_message = "₿ Par" + sigdata['Coin'] + '⚠⚠\n ➕ BBRSI {} \n ➕ EMARSI {} \n ➕ BINDHAST{} '.format(sigdata['BBRSI'],sigdata['EMARSI'],sigdata['BINDHAST'])
                        bot_chatID = str(df['chatid'][countid])
                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                        response = requests.get(send_text)
                        print(response.json())
        if usertype == "prem":
            for index, sigdata in pd.DataFrame(listpro).iterrows():
                print(sigdata['Coin'])
                IST = pytz.timezone('America/Bogota')
                e = datetime.datetime.now(IST)

                hours = getattr(e, 'hour')
                minutes = getattr(e, 'minute')
                second = getattr(e, 'second')
                days = getattr(e, 'day')
                month = getattr(e, 'month')
                year = getattr(e, 'year')

                dateup = str(year) + "-" + str(month) + "-" + str(days)
                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                    sigdata['Coin'], dateup)
                dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                verify = False

                if len(dfsigver) > 0:
                    hour = dfsigver['hour'].iloc[-1]
                    print('Hora pedido:', (hour))
                    time2 = pd.to_timedelta(hour)

                    # Tiempo seleccionado + 1 hs
                    time3 = pd.Timedelta(time2)
                    time4 = time3.total_seconds()
                    print('hora actualizaci0n:', (time4))
                    hoursd = (time4 // 3600) + 4
                    minutesd = (time4 % 3600) // 60
                    secondsd = time4 % 60
                    timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                    timeactdelta = pd.Timedelta(timeact)
                    timeactseconds = timeactdelta.total_seconds()

                    print('Hora vencimiento:', (timeactseconds))
                    d = datetime.datetime.now()

                    IST = pytz.timezone('America/Bogota')
                    e = datetime.datetime.now(IST)
                    print(e)

                    hoursact = getattr(e, 'hour')
                    minutesact = getattr(e, 'minute')
                    secondsact = getattr(e, 'second')

                    timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                    timeactualdelta = pd.Timedelta(timeactual)
                    timeactualseconds = timeactualdelta.total_seconds()
                    if timeactualseconds >= timeactseconds:
                        verify = True
                    else:
                        verify = False
                if verify == True:
                    bot_messagefull = "₿ Par" + sigdata['Coin'] + '⚠⚠\n ➕ BBRSI {} \n ➕ EMARSI {} \n ➕ BINDHAST {} \n ➕ EMARSICCI {}\n ➕ ADXMOMENTUM {}\n ➕ ADXSMAS {}'.format(sigdata['BBRSI'], sigdata['EMARSI'], sigdata['BINDHAST'],sigdata['EMARSICCI'], sigdata['ADXMOMENTUM'], sigdata['ADXSMAS'])
                    bot_chatID = str(df['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                    response = requests.get(send_text)
                    print(response.json())

        # return response.json()
        countid = countid + 1


def clear():
    os.system('clear')
    return


def verif_pos(data_comp, carry_obj, c_obj):
    carry = 1
    c1 = 0
    hab2 = False

    down_stat = 0
    up_stat = 0

    for x in data_comp:

        if carry == carry_obj and hab2 == False:
            print('Hemos encontrado un cambio en la posicion : ', carry_obj)

            if x == True:
                print(c1)
                print(x)
                print(c_obj)
                if c1 > c_obj:
                    print("DOWN")
                    down_stat = c1
                elif c1 < c_obj:
                    print("UP")
                    up_stat = c1
            hab2 = True
        c1 = c1 + 1

        if c1 > 10:
            c1 = 1
            carry = carry + 1
            if hab2 == True:
                hab2 = False
        elif hab2 == True:
            if x == True:
                print(c1)
                print(x)
                print(c_obj)
                if c1 > c_obj:
                    print("DOWN")
                    down_stat = c1
                elif c1 < c_obj:
                    print("UP")
                    up_stat = c1

    return (down_stat, up_stat)


def verif_pos_25(data_comp2, data_porcen, carry_obj2, c_obj2):
    carry = 1
    c1 = 0
    hab2 = False

    down_stat2 = 0
    up_stat2 = 0
    up_porc2 = 0
    up_porc2v = 0.0
    down_porc2 = 0
    down_porc2v = 0.0

    for x in data_comp2:

        if carry == carry_obj2 and hab2 == False:
            print('Hemos encontrado un cambio en la posicion : ', carry_obj2)

            if x == True:
                print(c1)
                print(x)
                print(c_obj2)
                if c1 > c_obj2:
                    print("DOWN")
                    down_stat2 = c1
                    carry_por = 1
                    c_por = 0
                    hab_por = False
                    for y in data_porcen:
                        c_por = c_por + 1
                        if c_por > 25:
                            c_por = 1
                            carry_por = carry_por + 1

                        if carry_por == carry_obj2 and c_por == c1:
                            print("Update porcentaje in ")
                            print(c1)
                            print(y)
                            down_porc2 = c_por
                            down_porc2v = y

                elif c1 < c_obj2:
                    print("UP")
                    up_stat2 = c1
                    carry_por = 1
                    c_por = 0
                    hab_por = False
                    for y in data_porcen:
                        c_por = c_por + 1
                        if c_por > 25:
                            c_por = 1
                            carry_por = carry_por + 1

                        if carry_por == carry_obj2 and c_por == c1:
                            print("Update porcentaje in ")
                            print(c1)
                            print(y)
                            up_porc2 = c_por
                            up_porc2v = y

            hab2 = True
        c1 = c1 + 1

        if c1 > 25:
            c1 = 1
            carry = carry + 1
            if hab2 == True:
                hab2 = False
        elif hab2 == True:
            if x == True:
                print(c1)
                print(x)
                print(c_obj2)
                if c1 > c_obj2:
                    print("DOWN")
                    down_stat2 = c1
                    carry_por = 1
                    c_por = 0
                    hab_por = False
                    for y in data_porcen:
                        c_por = c_por + 1
                        if c_por > 25:
                            c_por = 1
                            carry_por = carry_por + 1

                        if carry_por == carry_obj2 and c_por == c1:
                            print("Update porcentaje in ")
                            print(c1)
                            print(y)
                            down_porc2 = c_por
                            down_porc2v = y

                elif c1 < c_obj2:
                    print("UP")
                    up_stat2 = c1
                    carry_por = 1
                    c_por = 0
                    hab_por = False
                    for y in data_porcen:
                        c_por = c_por + 1
                        if c_por > 25:
                            c_por = 1
                            carry_por = carry_por + 1

                        if carry_por == carry_obj2 and c_por == c1:
                            print("Update porcentaje in ")
                            print(c1)
                            print(y)
                            up_porc2 = c_por
                            up_porc2v = y

    return (down_stat2, up_stat2, up_porc2, up_porc2v, down_porc2, down_porc2v)


if __name__ == "__main__":
    while True:
        command = 'python3 /home/ec2-user/Desktop/Pattern/best_coins_usdt.py'
        os.system(command)
        mariadb_connection = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                             database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
        cursor = mariadb_connection.cursor()
        query = "SELECT * FROM topcoinsu;"
        df = pd.read_sql_query(query, mariadb_connection)
        query2 = "SELECT * FROM top25coinsu;"
        df_25 = pd.read_sql_query(query2, mariadb_connection)
        print('Recopilando datos iniciales.....')
        print('---------------------Tiempo de Actualizacion-----------------------')
        print('--------------------------------------------')

        for x in range(0, 159):
            if x == 0:
                countx = 0
                seg = 0

                minute = 0
            elif seg >= 1:
                countx = seg

            #print('Minutes:' + '%.2f' % minute + ' Segundos :' + '%.2f' % seg)
            seg = seg + 1

            if seg >= 60:
                seg = 0
                minute = minute + 1
            time.sleep(1)
            #clear()
        command = 'python3 /home/ec2-user/Desktop/Pattern/best_coins_usdt.py'
        os.system(command)
        mariadb_connection = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                             database='agarjoya_bitpattern', host='127.0.0.1', port='3306')
        cursor = mariadb_connection.cursor()

        query = "SELECT * FROM topcoinsu;"
        df1 = pd.read_sql_query(query, mariadb_connection)
        query2 = "SELECT * FROM top25coinsu;"
        df1_25 = pd.read_sql_query(query2, mariadb_connection)
        print('---------------------2 list-----------------------')
        print(df_25)
        print('--------------------------------------------')
        print(df1_25)
        sleep(1)

        comparisons = [a == b for (a, b) in itertools.product(df['coin_name'], df1['coin_name'])]

        comparisons2 = [a == b for (a, b) in itertools.product(df_25['coin_name'], df1_25['coin_name'])]

        comparisons1 = [b - a for (a, b) in itertools.product(df_25['porcentaje'], df1_25['porcentaje'])]

        carry = 1
        compresult = []
        stable_stat = []
        up_stat_com = []
        down_stat_com = []
        c = 0
        hab = 1

        for x in comparisons:
            c = c + 1
            if (c == carry) and (hab == 1):
                compresult.append(x)
                if x == 0:
                    (down_stat, up_stat) = verif_pos(comparisons, carry, c)
                    up_stat_com.append(up_stat)
                    down_stat_com.append(down_stat)


                else:
                    stable_stat.append(carry)
                carry = carry + 1
                hab = 0
            elif c > 10:
                c = 1
                hab = 1

        #print(compresult)
        #print(stable_stat)
        #print(up_stat_com)
        #print(down_stat_com)

        carry2 = 1
        compresult2 = []
        stable_stat2 = []
        up_stat_com2 = []
        down_stat_com2 = []
        up_porc2_com = []
        up_porc2v_com = []
        down_porc2_com = []
        down_porc2v_com = []
        c2 = 0
        hab2 = 1

        for x2 in comparisons2:
            c2 = c2 + 1
            if (c2 == carry2) and (hab2 == 1):
                compresult2.append(x2)
                if x2 == 0:
                    (down_stat2, up_stat2, up_porc2, up_porc2v, down_porc2, down_porc2v) = verif_pos_25(comparisons2,
                                                                                                        comparisons1,
                                                                                                        carry2, c2)
                    up_stat_com2.append(up_stat2)
                    down_stat_com2.append(down_stat2)
                    up_porc2_com.append(up_porc2)
                    # if up_porc2v != 0.0:
                    up_porc2v_com.append(up_porc2v)
                    down_porc2_com.append(down_porc2)
                    down_porc2v_com.append(down_porc2v)

                else:
                    stable_stat2.append(carry2)
                carry2 = carry2 + 1
                hab2 = 0
            elif c2 > 25:
                c2 = 1
                hab2 = 1

        #print(compresult2)
        #print(stable_stat2)
        #print(up_stat_com2)
        #print(down_stat_com2)
        #print(up_porc2_com)
        #print(up_porc2v_com)
        #print(down_porc2_com)
        #print(down_porc2v_com)

        count = 0
        for valor in df1['coin_name']:
            count = count + 1
            cursor.execute("""UPDATE top_10_compu SET coin_name = %s WHERE coin_id = %s""", (valor, count))
            mariadb_connection.commit()

        count1 = 0
        for valor1 in df1['porcentaje']:
            count1 = count1 + 1
            cursor.execute("""UPDATE top_10_compu SET porcentaje = %s WHERE coin_id = %s""", (valor1, count1))
            mariadb_connection.commit()

        count2 = 0
        for valor2 in compresult:
            count2 = count2 + 1
            cursor.execute("""UPDATE top_10_compu SET status = %s WHERE coin_id = %s""", (valor2, count2))
            mariadb_connection.commit()

        count3 = 0
        for valor3 in stable_stat:
            cursor.execute("""UPDATE top_10_compu SET tend = %s WHERE coin_id = %s""", ("STABLE", valor3))
            mariadb_connection.commit()

        count4 = 0
        for valor4 in up_stat_com:
            cursor.execute("""UPDATE top_10_compu SET tend = %s WHERE coin_id = %s""", ("UP", valor4))
            mariadb_connection.commit()

        count5 = 0
        for valor5 in down_stat_com:
            cursor.execute("""UPDATE top_10_compu SET tend = %s WHERE coin_id = %s""", ("DOWN", valor5))
            mariadb_connection.commit()

        count6 = 0
        for valor6 in stable_stat2:
            cursor.execute("""UPDATE top_25_coins_newu SET status = %s WHERE coin_id = %s""", ("STABLE", valor6))
            mariadb_connection.commit()

        count7 = 0
        for valor7 in up_stat_com2:
            cursor.execute("""UPDATE top_25_coins_newu SET status = %s WHERE coin_id = %s""", ("UP", valor7))
            mariadb_connection.commit()

        count8 = 0
        for valor8 in down_stat_com2:
            cursor.execute("""UPDATE top_25_coins_newu SET status = %s WHERE coin_id = %s""", ("DOWN", valor8))
            mariadb_connection.commit()

        count9 = -1
        for valor9 in up_porc2_com:
            count9 = count9 + 1
            cursor.execute("""UPDATE top_25_coins_newu SET porcomp = %s WHERE coin_id = %s""",
                           (up_porc2v_com[count9], valor9))
            mariadb_connection.commit()

        count10 = -1
        for valor10 in down_porc2_com:
            count10 = count10 + 1
            cursor.execute("""UPDATE top_25_coins_newu SET porcomp = %s WHERE coin_id = %s""",
                           (down_porc2v_com[count10], valor10))
            mariadb_connection.commit()

        query = "SELECT * FROM top_10_compu;"
        dat_1 = pd.read_sql_query(query, mariadb_connection)
        print('---------------------10 comlist-----------------------')
        print(dat_1)
        sleep(15)

        query2 = "SELECT * FROM top_25_coins_newu;"
        dat_2 = pd.read_sql_query(query2, mariadb_connection)
        print('---------------------25 comlist-----------------------')
        print(dat_2)

        query3 = "SELECT * FROM top25coinspu;"
        dat_3 = pd.read_sql_query(query3, mariadb_connection)
        print('---------------------25 comlist perdida-----------------------')
        print(dat_3)
        countcoin2 = 0
        listprop = []
        listpro2p = []
        for y in range(len(dat_3)):
            coin_name = dat_3['coin_name'][countcoin2]
            tend = dat_3['status'][countcoin2]

            print(coin_name)

            if coin_name == 'ARKMUSDT':
                continue


            #df = client.get_historical_klines(symbol=coin_name + "BTC", interval='1h', start_str='5 days ago UTC')
            #df = client.get_historical_klines(symbol=coin_name, interval='5m', start_str='1 days ago UTC')
            #kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?symbol={symbol}&interval=4h&limit=100'
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
            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
            print(kline_url)
            kline_response = requests.get(kline_url)
            kline_data = kline_response.json()
            #print(kline_data['result']['list'])
            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
            df2 = pd.DataFrame(kline_data['result']['list'])
            
            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
            df2.set_index('Open time', inplace=True)
            df2['Close'] = df2[4].astype(float)
            df2['High'] = df2[2].astype(float)
            df2['Low'] = df2[3].astype(float)
            df2['Open'] = df2[1].astype(float)
            df2 = df2.iloc[::-1]
            #df2 = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
            #                                'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
            #                                'Taker buy quote asset volume', 'Ignore'])
            #print(df2)

            print(strat_EMA_RSI(df2))

            try:

                if strat_EMA_RSI(df2) != "❌":
                    #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
                    #os.system(f'start cmd /c "{command}"')
                    #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                    #os.system(f'start cmd /c "{command2}"')
                    command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'moving_average')
                    os.system(command)

                    command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                    os.system(command2)

                    #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                    #os.system(command3)
                #    subprocess.Popen(['C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe', 'e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py', f'{coin_name}/USDT'])
                if strat_EMA_RSI_CCI(df2) != "❌":
                    #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
                    #os.system(f'start cmd /c "{command}"')
                    #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                    #os.system(f'start cmd /c "{command2}"')
                    command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'ema_rsi_cci')
                    os.system(command)

                    command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                    os.system(command2)

                    #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                    #os.system(command3)
                if strat_EMA_RSI(df2) != "❌" or strat_EMA_RSI_CCI(
                            df2) != "❌" or strat_BB_RSI(df2) != "❌" or strat_ADX_MOMENTUM(
                            df2) != "❌" or strat_ADX_SMAS(df2) != "❌":
                    listprop.append(
                        {
                            'Coin': coin_name,
                            'BBRSI': strat_BB_RSI(df2),
                            'EMARSI': strat_EMA_RSI(df2),
                            'EMARSICCI': strat_EMA_RSI_CCI(df2),
                            'ADXMOMENTUM': strat_ADX_MOMENTUM(df2),
                            'ADXSMAS': strat_ADX_SMAS(df2),
                        }
                    )
                if strat_EMA_RSI(df2) != "❌" or strat_BINDHAST(df2) != "❌" or strat_BB_RSI(df2) != "❌":
                    listpro2p.append(
                        {
                            'Coin': coin_name,
                            'BBRSI': strat_BB_RSI(df2),
                            'EMARSI': strat_EMA_RSI(df2),
                            'BINDHAST': strat_BINDHAST(df2),

                        }
                    )
            except:
                pass
            countcoin2 = countcoin2 + 1


        countcoin = 0
        listpro =[]
        listpro2 = []
        for y in range(len(dat_2)):
            coin_name = dat_2['coin_name'][countcoin]
            tend = dat_2['status'][countcoin]
            if coin_name == 'ARKMUSDT':
                continue
            if tend == "UP":
                print(coin_name)
                #df = client.get_historical_klines(symbol=coin_name, interval='5m', start_str='1 days ago UTC')

                #df2 = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                #                                'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                #                                'Taker buy quote asset volume', 'Ignore'])
                #kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?symbol={symbol}&interval=4h&limit=100'
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
                kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                kline_response = requests.get(kline_url)
                kline_data = kline_response.json()
            #print(kline_data['result']['list'])
                #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                df2 = pd.DataFrame(kline_data['result']['list'])
                df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                df2.set_index('Open time', inplace=True)
                df2['Close'] = df2[4].astype(float)
                df2['High'] = df2[2].astype(float)
                df2['Low'] = df2[3].astype(float)
                df2['Open'] = df2[1].astype(float)
                df2 = df2.iloc[::-1]
                #print(df2)
                #print(strat_EMA_RSI(df2))
                #print(strat_BINDHAST(df2))
                #print(strat_EMA_RSI_CCI(df2))
                #print(strat_BB_RSI(df2))
                #print(strat_ADX_MOMENTUM(df2))
                #print(strat_ADX_SMAS(df2))
                try:
                    if strat_EMA_RSI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'moving_average')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        #os.system(command3)
                    if strat_EMA_RSI_CCI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'ema_rsi_cci')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        #os.system(command3)
                        #os.system('C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py {}'.format(coin_name + "/USDT"))
                    #    subprocess.Popen(['C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe', 'e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py', f'{coin_name}/USDT'])
                    if strat_EMA_RSI(df2) != "❌" or strat_EMA_RSI_CCI(
                            df2) != "❌" or strat_BB_RSI(df2) != "❌" or strat_ADX_MOMENTUM(
                            df2) != "❌" or strat_ADX_SMAS(df2) != "❌":
                        listpro.append(
                            {
                                'Coin': coin_name,
                                'BBRSI': strat_BB_RSI(df2),
                                'EMARSI': strat_EMA_RSI(df2),
                                'EMARSICCI': strat_EMA_RSI_CCI(df2),
                                'ADXMOMENTUM': strat_ADX_MOMENTUM(df2),
                                'ADXSMAS': strat_ADX_SMAS(df2),
                            }
                        )
                    if strat_EMA_RSI(df2) != "❌" or strat_BINDHAST(df2) != "❌" or strat_BB_RSI(df2) != "❌":
                        listpro2.append(
                            {
                                'Coin': coin_name,
                                'BBRSI': strat_BB_RSI(df2),
                                'EMARSI': strat_EMA_RSI(df2),
                                'BINDHAST': strat_BINDHAST(df2),

                            }
                        )
                except:
                    pass
            elif tend == "STABLE":
                print(coin_name)
                #df = client.get_historical_klines(symbol=coin_name, interval='5m', start_str='1 days ago UTC')

                #df2 = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                #                                'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                #                                'Taker buy quote asset volume', 'Ignore'])
                #kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?symbol={symbol}&interval=4h&limit=100'
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
                kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                kline_response = requests.get(kline_url)
                kline_data = kline_response.json()
            #print(kline_data['result']['list'])
                #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                df2 = pd.DataFrame(kline_data['result']['list'])
                df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                df2.set_index('Open time', inplace=True)
                df2['Close'] = df2[4].astype(float)
                df2['High'] = df2[2].astype(float)
                df2['Low'] = df2[3].astype(float)
                df2['Open'] = df2[1].astype(float)
                df2 = df2.iloc[::-1]
                #print(df2)
                #print(strat_EMA_RSI(df2))
                #print(strat_BINDHAST(df2))
                #print(strat_EMA_RSI_CCI(df2))
                #print(strat_BB_RSI(df2))
                #print(strat_ADX_MOMENTUM(df2))
                #print(strat_ADX_SMAS(df2))
                try:
                    if strat_EMA_RSI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'moving_average')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        #os.system(command3)
                    if strat_EMA_RSI_CCI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'ema_rsi_cci')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        #os.system(command3)
                        #os.system('C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py {}'.format(coin_name + "/USDT"))
                    #    subprocess.Popen(['C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe', 'e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py', f'{coin_name}/USDT'])
                    if strat_EMA_RSI(df2) != "❌" or strat_EMA_RSI_CCI(
                            df2) != "❌" or strat_BB_RSI(df2) != "❌" or strat_ADX_MOMENTUM(
                            df2) != "❌" or strat_ADX_SMAS(df2) != "❌":
                        listpro.append(
                            {
                                'Coin': coin_name,
                                'BBRSI': strat_BB_RSI(df2),
                                'EMARSI': strat_EMA_RSI(df2),
                                'EMARSICCI': strat_EMA_RSI_CCI(df2),
                                'ADXMOMENTUM': strat_ADX_MOMENTUM(df2),
                                'ADXSMAS': strat_ADX_SMAS(df2),
                            }
                        )
                    if strat_EMA_RSI(df2) != "❌" or strat_BINDHAST(df2) != "❌" or strat_BB_RSI(df2) != "❌":
                        listpro2.append(
                            {
                                'Coin': coin_name,
                                'BBRSI': strat_BB_RSI(df2),
                                'EMARSI': strat_EMA_RSI(df2),
                                'BINDHAST': strat_BINDHAST(df2),

                            }
                        )
                except:
                    pass



            elif tend == "DOWN":
                print(coin_name)
                #df = client.get_historical_klines(symbol=coin_name, interval='5m', start_str='1 days ago UTC')

                #df2 = pd.DataFrame(df, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                #                                'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                #                                'Taker buy quote asset volume', 'Ignore'])
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
                kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                kline_response = requests.get(kline_url)
                kline_data = kline_response.json()
                #print(kline_data['result']['list'])
                #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                df2 = pd.DataFrame(kline_data['result']['list'])
                df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                df2.set_index('Open time', inplace=True)
                df2['Close'] = df2[4].astype(float)
                df2['High'] = df2[2].astype(float)
                df2['Low'] = df2[3].astype(float)
                df2['Open'] = df2[1].astype(float)
                df2 = df2.iloc[::-1]
                #print(df2)
                #print(strat_EMA_RSI(df2))
                #print(strat_BINDHAST(df2))
                #print(strat_EMA_RSI_CCI(df2))
                #print(strat_BB_RSI(df2))
                #print(strat_ADX_MOMENTUM(df2))
                #print(strat_ADX_SMAS(df2))
                try:
                    if strat_EMA_RSI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'moving_average')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'moving_average')
                        #os.system(command3)
                        #subprocess.Popen(['C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe', 'e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py', f'{coin_name}/USDT'])
                        #os.system('C:/Users/bitpa/AppData/Local/Microsoft/WindowsApps/python3.10.exe e:/Proyectos/patternbtcapp/patternbtcapp/bybytbot.py {}'.format(coin_name + "/USDT"))
                    if strat_EMA_RSI_CCI(df2) != "❌":
                        #command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
                        #os.system(f'start cmd /c "{command}"')
                        #command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
                        #os.system(f'start cmd /c "{command2}"')
                        command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {} {}'.format(coin_name.replace('USDT','') + "/USDT", 'ema_rsi_cci')
                        os.system(command)

                        command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        os.system(command2)

                        #command3 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot3.py {} {}'.format(coin_name.replace('USDT','')  + "/USDT", 'ema_rsi_cci')
                        #os.system(command3)
                    if strat_EMA_RSI(df2) != "❌" or strat_EMA_RSI_CCI(
                            df2) != "❌" or strat_BB_RSI(df2) != "❌" or strat_ADX_MOMENTUM(
                            df2) != "❌" or strat_ADX_SMAS(df2) != "❌":
                        listpro.append(
                            {
                                'Coin': coin_name,
                                'BBRSI': strat_BB_RSI(df2),
                                'EMARSI': strat_EMA_RSI(df2),
                                'EMARSICCI': strat_EMA_RSI_CCI(df2),
                                'ADXMOMENTUM': strat_ADX_MOMENTUM(df2),
                                'ADXSMAS': strat_ADX_SMAS(df2),
                            }
                        )
                    if strat_EMA_RSI(df2) != "❌" or strat_BINDHAST(df2) != "❌" or strat_BB_RSI(df2) != "❌":
                        listpro2.append(
                            {
                            'Coin': coin_name,
                            'BBRSI': strat_BB_RSI(df2),
                            'EMARSI': strat_EMA_RSI(df2),
                            'BINDHAST': strat_BINDHAST(df2),

                            }
                        )
                except:
                    pass
            countcoin = countcoin + 1

        
        
        #print(pd.Series(listpro))
        # Seleccionar tiempo actualizado
        query = "SELECT twitter_time1 FROM topcoinsu;"
        df = pd.read_sql_query(query, mariadb_connection)
        d1 = pd.DataFrame(df)
        time1n = d1['twitter_time1'][0]
        time2n = pd.to_timedelta(time1n)

        # Tiempo seleccionado + 1 hs
        time3n = pd.Timedelta(time2n)
        time4new = time3n.total_seconds()
        print('hora actualizaci0n:', (time4new))
        hoursdn = (time4new // 3600) + 1
        minutesdn = (time4new % 3600) // 60
        secondsdn = time4new % 60
        timeactn = timedelta(hours=hoursdn, minutes=minutesdn, seconds=secondsdn)
        timeactdeltan = pd.Timedelta(timeactn)
        timeactsecondsnew = timeactdeltan.total_seconds()

        print('hora Nueva:', (timeactsecondsnew))

        # Tiempo actual a comparar

        dn = datetime.datetime.now()
        # for attr in [ 'hour', 'minute', 'second']:
        #	print attr, ':', getattr(d, attr)

        hoursactn = getattr(dn, 'hour')
        minutesactn = getattr(dn, 'minute')
        secondsactn = getattr(dn, 'second')

        timeactualn = timedelta(hours=hoursactn, minutes=minutesactn, seconds=secondsactn)
        timeactualdeltan = pd.Timedelta(timeactualn)
        timeactualsecondsnew = timeactualdeltan.total_seconds()

        listmov = pd.DataFrame(listpro)
        listmovp = pd.DataFrame(listprop)
        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
        
        query = "SELECT chatid, type FROM users;"
        dfuser = pd.read_sql_query(query, mariadb_connection)
        countid = 0
        print(type(listmovp))
        print(listmovp.columns)
        print(listmovp)
        print(listmov)
        for x in range(len(dfuser)):

            usertype = dfuser['type'][countid]

            if usertype == "free":
                bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                bot_chatID = str(dfuser['chatid'][countid])
                send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                response = requests.get(send_text)
            if usertype == "prem":
                # Assuming 'listmovp' is your DataFrame

                if not listmovp.empty:
                    col_names = list(listmovp.columns[:3])

                    # Create a new dataframe with the headers and data
                    data = [col_names] + list(listmovp[listmovp.columns[:3]].values)
                    df_table = pd.DataFrame(data)

                    # Convert dataframe to a string table using the 'prettytable' module
                    #table = prettytable.PrettyTable(format=True, print_empty=False, tablefmt="simple")
                    #table.field_names = col_names
                    #for row in listmovp[listmovp.columns[:3]].values:
                    #    table.add_row(row)
                    # Convert the DataFrame to a table using the tabulate package
                    table = tabulate.tabulate(listmovp[listmovp.columns[:3]], headers='keys', tablefmt='simple')
                    table2 = tabulate.tabulate(listmovp[listmovp.columns[3:6]], headers='keys', tablefmt='simple')
                    #table = table.replace('|-', '| ').replace('-|', '| ').replace('-', ' ').replace('=', '')
                    # Assuming your DataFrame is called "df"
                    #table = tabulate.tabulate(listmovp, headers='keys', tablefmt='pipe', colalign=('center',)*len(col_names))

                    # Calculate the maximum length of the content in each column
                    #max_lens = [max([len(str(row[col])) for row in listmovp] + [len(col)]) for col in col_names]
                    #max_lens = [max([len(str(row[col])) for row in listmovp.loc[:, col]] + [len(col)]) for col in col_names]
                    #max_lens = [max([len(str(row[col])) for row in listmovp.iloc[:, listmovp.columns.get_loc(col)]] + [len(col)]) for col in col_names]
                    #max_lens = [max([len(str(row[col])) for row in listmovp.iloc[:, i]] + [len(col)]) for i, col in enumerate(col_names)]

                    #max_lens = [max([len(str(row[j])) for row in listmovp.iloc[:, i]] + [len(col_names[i])]) for i, j in enumerate(range(len(col_names)))]
                    # Set the column widths to the maximum lengths
                    #col_widths = [f'{max_lens[i]}:{max_lens[i]}' for i in range(len(col_names))]

                    # Use the col_widths parameter to adjust the column widths in the table
                    #table = tabulate.tabulate(listmovp, headers='keys', tablefmt='pipe', colalign=('center',)*len(listmovp.columns), colwidths=col_widths)

                    # Split the table into chunks of 4096 characters (Telegram message length limit)
                    #chunks = textwrap.wrap(table, width=4096)

                    # Send each chunk as a separate message to Telegram
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #for chunk in chunks:
                    #    bot_message = f"{chunk}"
                    #    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    #    response = requests.get(send_text)
                    #    print(response.json())
                    #table_string = tabulate.tabulate(listmovp, headers='keys', tablefmt='pipe', colalign=('center',)*len(listmovp.columns))

                    # Split the table into chunks of 4096 characters (Telegram message length limit)
                    #chunks = textwrap.wrap(table_string, width=4096)

                    # Send each chunk as a separate message to Telegram
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #for chunk in chunks:
                    #    bot_message = f"Activos En perdida:\n\n{chunk}"
                    #    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    #    response = requests.get(send_text)
                    bot_message = "Activos En perdida "
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)

                    bot_message = f"{table}"
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    bot_message = f"{table2}"
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)

                    
                    #print(response.json())
                    #bot_messagefull = "Activos En perdida \n" + listmovp.to_string()
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                    #response = requests.get(send_text)
                if not listmov.empty:
                    col_names = list(listmov.columns[:3])

                    # Create a new dataframe with the headers and data
                    data = [col_names] + list(listmov[listmov.columns[:3]].values)
                    df_table = pd.DataFrame(data)
                    # Assuming your DataFrame is 
# Convert dataframe to a string table using the 'prettytable' module
                    #table = prettytable.PrettyTable(format=True, print_empty=False, tablefmt="simple")
                    #table.field_names = col_names
                    #for row in listmov[listmov.columns[:3]].values:
                    #    table.add_row(row)
                    #table = tabulate.tabulate(listmov[listmov.columns[:5]], headers='keys', tablefmt='simple')
                    table = tabulate.tabulate(listmov[listmov.columns[:3]], headers='keys', tablefmt='simple')
                    table2 = tabulate.tabulate(listmov[listmov.columns[3:6]], headers='keys', tablefmt='simple')
                    #table = table.replace('|-', '| ').replace('-|', '| ').replace('-', ' ').replace('=', '')
                    #table = tabulate.tabulate(listmov, headers='keys', tablefmt='pipe', colalign=('center',)*len(col_names))

                    # Calculate the maximum length of the content in each column
                    #max_lens = [max([len(str(row[col])) for row in listmov] + [len(col)]) for col in col_names]
                    #ax_lens = [max([len(str(row[col])) for row in listmov.loc[:, col]] + [len(col)]) for col in col_names]
                    #max_lens = [max([len(str(row[col])) for row in listmov.iloc[:, listmov.columns.get_loc(col)]] + [len(col)]) for col in col_names]
                    #max_lens = [max([len(str(row[col])) for row in listmov.iloc[:, i]] + [len(col)]) for i, col in enumerate(col_names)]
                    #max_lens = [max([len(str(row[col])) for row in listmov.iloc[:, i]] + [len(col)]) for i, col in enumerate(col_names)]
                    #max_lens = [max([len(str(row[j])) for row in listmov.iloc[:, i]] + [len(col_names[i])]) for i, j in enumerate(range(len(col_names)))]
                    # Set the column widths to the maximum lengths
                    #col_widths = [f'{max_lens[i]}:{max_lens[i]}' for i in range(len(col_names))]

                    # Use the col_widths parameter to adjust the column widths in the table
                    #table = tabulate.tabulate(listmov, headers='keys', tablefmt='pipe', colalign=('center',)*len(listmov.columns), colwidths=col_widths)

                    # Split the table into chunks of 4096 characters (Telegram message length limit)
                    #chunks = textwrap.wrap(table, width=4096)

                    # Send each chunk as a separate message to Telegram
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #for chunk in chunks:
                    #    bot_message = f"{chunk}"
                    #    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    #    response = requests.get(send_text)
                    #    print(response.json())
                    #table_string2 = tabulate.tabulate(listmov, headers='keys', tablefmt='pipe', colalign=('center',)*len(listmov.columns))
                    # Split the table into chunks of 4096 characters (Telegram message length limit)
                    #chunks = textwrap.wrap(table_string2, width=4096)

                    # Send each chunk as a separate message to Telegram
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #for chunk in chunks:
                    #    bot_message = f"Activos AL ALza:\n\n{chunk}"
                    #    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    #    response = requests.get(send_text)
                    bot_message = "Activos AL ALza "
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    bot_message = f"{table}"
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    bot_message = f"{table2}"
                    bot_chatID = str(dfuser['chatid'][countid])
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                    response = requests.get(send_text)
                    #print(response.json())

                    #bot_messagefull = "Activos AL ALza \n" + listmov.to_string()
                    #bot_chatID = str(dfuser['chatid'][countid])
                    #send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                    #response = requests.get(send_text)
                    #print(response.json())
            

            countid = countid + 1

        if len(listmovp.index) > 0:

            for index, sigdata in pd.DataFrame(listprop).iterrows():

                coin_name = sigdata['Coin']


                if (sigdata == "🔴 Venta").sum() > 0 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        print(kline_url)
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        print(df2['Close'])
                        
                        pe = float(df2['Close'].iloc[-1])
                        print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0

                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin,type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True


                        cursor1 = mariadb_connection1.cursor()

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Alto",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()

                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Alto",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()

                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 0 and (sigdata == "🔴 Venta").sum() == 0:
                    try:
                        
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.02)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)
                        print(sigdata['Coin'])

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status != 'Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False
                        print(dfsigver)

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]

                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()

                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()


                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)


                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True
                        print(verify)

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                   start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                    columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                             'Close time',
                            #                             'Quote asset volume', 'Number of trades',
                            #                             'Taker buy base asset volume',
                            #                             'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc



                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)


                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Alto",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Alto",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)


                if (sigdata == "🔴 Venta").sum() > 1 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Medio",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Medio",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 1 and (sigdata == "🔴 Venta").sum() == 0:
                    try:

                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.02)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                      start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                       columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                                'Close time',
                            #                                'Quote asset volume', 'Number of trades',
                            #                                'Taker buy base asset volume',
                            #                                'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc

                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Medio",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Medio",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)
                if (sigdata == "🔴 Venta").sum() > 2 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True
                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Bajo",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Bajo",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 2 and (sigdata == "🔴 Venta").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.01)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='mlm', host='127.0.0.1',
                                                              port='3306')

                        cursor2 = mariadb_connection2.cursor()
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(sigdata['Coin'],dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)
                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                      start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                       columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                                'Close time',
                            #                                'Quote asset volume', 'Number of trades',
                            #                                'Taker buy base asset volume',
                            #                                'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc

                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Bajo",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()


                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Bajo",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

        if len(listmov.index) > 0:

            for index, sigdata in pd.DataFrame(listpro).iterrows():
                #print((sigdata == "🔴 Venta").sum())
                #print((sigdata == "❌").sum())
                #print((sigdata == "🟢 Compra").sum())
                coin_name = sigdata['Coin']

                if (sigdata == "🔴 Venta").sum() > 0 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        print(kline_url)
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        print(df2['Close'])
                        pe = float(df2['Close'].iloc[-1])
                        print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0

                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True
                        cursor1 = mariadb_connection1.cursor()

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Alto",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()

                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Alto",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()

                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 0 and (sigdata == "🔴 Venta").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.02)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                      start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                       columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                                'Close time',
                            #                                'Quote asset volume', 'Number of trades',
                            #                                'Taker buy base asset volume',
                            #                                'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc

                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Alto",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Alto",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)

                if (sigdata == "🔴 Venta").sum() > 1 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True
                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Medio",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Medio",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 1 and (sigdata == "🔴 Venta").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.02)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                      start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                       columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                                'Close time',
                            #                                'Quote asset volume', 'Number of trades',
                            #                                'Taker buy base asset volume',
                            #                                'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc

                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                 #       symbol=sigdata['Coin'],
                                 #       side='BUY',
                                 ##       type='LIMIT',
                                 #       timeInForce='GTC',
                                 #       quantity=float(amt_str),
                                 #       price=amt_str2)
                                 #   print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Medio",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Medio",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)
                if (sigdata == "🔴 Venta").sum() > 2 and (sigdata == "🟢 Compra").sum() == 0:
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        sl = pe + (pe * 0.01)
                        tp = pe - (pe * 0.02)

                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')

                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False
                        else:
                            verify = True
                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Bajo",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🔴 Venta", tp, sl, dateup,
                                 "Bajo",
                                 pe, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                        "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1

                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)

                if (sigdata == "🟢 Compra").sum() > 2 and (sigdata == "🔴 Venta").sum() == 0:#
                    try:
                        current_datetime = datetime.datetime.now()

                        # Set the start time to 12:00 AM (00:00:00) 7 days ago
                        start_datetime = current_datetime - datetime.timedelta(days=1)
                        start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                        # Set the end time to the current date and time
                        end_datetime = current_datetime

                        # Convert the datetime objects to timestamps in milliseconds
                        start_timestamp = int(start_datetime.timestamp() * 1000)
                        end_timestamp = int(end_datetime.timestamp() * 1000)
                        kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                        kline_response = requests.get(kline_url)
                        kline_data = kline_response.json()
                        #print(kline_data['result']['list'])
                        #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                        df2 = pd.DataFrame(kline_data['result']['list'])
                        df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                        df2.set_index('Open time', inplace=True)
                        df2['Close'] = df2[4].astype(float)
                        df2['High'] = df2[2].astype(float)
                        df2['Low'] = df2[3].astype(float)
                        df2['Open'] = df2[1].astype(float)
                        #print(df2['Close'].iloc[-1])
                        pe = float(df2['Close'].iloc[-1])
                        # print(pe)
                        penew = pe - (pe * 0.005)
                        sl = penew - (penew * 0.02)
                        tp = penew + (penew * 0.01)
                        bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                        # bot_chatID = '-1101441080121'
                        mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                              database='agarjoya_bitpattern', host='127.0.0.1',
                                                              port='3306')
                        query = "SELECT chatid, type FROM users;"
                        dfuser = pd.read_sql_query(query, mariadb_connection1)
                        countid = 0
                        IST = pytz.timezone('America/Bogota')
                        e = datetime.datetime.now(IST)

                        hours = getattr(e, 'hour')
                        minutes = getattr(e, 'minute')
                        second = getattr(e, 'second')
                        days = getattr(e, 'day')
                        month = getattr(e, 'month')
                        year = getattr(e, 'year')

                        dateup = str(year) + "-" + str(month) + "-" + str(days)
                        hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                        query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsig = pd.read_sql_query(query2, mariadb_connection1)

                        cursor1 = mariadb_connection1.cursor()

                        query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                            sigdata['Coin'], dateup)
                        dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                        verify = False

                        if len(dfsigver) > 0:
                            hour = dfsigver['hour'].iloc[-1]
                            print('Hora pedido:', (hour))
                            time2 = pd.to_timedelta(hour)

                            # Tiempo seleccionado + 1 hs
                            time3 = pd.Timedelta(time2)
                            time4 = time3.total_seconds()
                            print('hora actualizaci0n:', (time4))
                            hoursd = (time4 // 3600) + 4
                            minutesd = (time4 % 3600) // 60
                            secondsd = time4 % 60
                            timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                            timeactdelta = pd.Timedelta(timeact)
                            timeactseconds = timeactdelta.total_seconds()

                            print('Hora vencimiento:', (timeactseconds))
                            d = datetime.datetime.now()

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)
                            print(e)

                            hoursact = getattr(e, 'hour')
                            minutesact = getattr(e, 'minute')
                            secondsact = getattr(e, 'second')

                            timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                            timeactualdelta = pd.Timedelta(timeactual)
                            timeactualseconds = timeactualdelta.total_seconds()
                            if timeactualseconds >= timeactseconds:
                                verify = True
                            else:
                                verify = False

                        if len(dfsig) == 0 and verify == True:
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)
                            # balance = client.get_asset_balance(asset='BTC')

                            # dfbtc = client.get_historical_klines(symbol="BTCUSDT", interval='15m',
                            #                                      start_str='1 days ago UTC')

                            # df2btc = pd.DataFrame(dfbtc,
                            #                       columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                            #                                'Close time',
                            #                                'Quote asset volume', 'Number of trades',
                            #                                'Taker buy base asset volume',
                            #                                'Taker buy quote asset volume', 'Ignore'])

                            # pebtc = float(df2btc['Close'].iloc[-1])

                            # qtytc = 10 / pebtc

                            # print(balance['free'])
                            # print(qtytc)

                            # if float(balance['free']) > 0 and float(balance['free'] > float(qtytc)):

                            #     qty = float(qtytc) / float(penew)

                            #     exch = client.get_exchange_info()
                            #     pqty = 0
                            #     pprice = 0

                            #     for symbol in exch['symbols']:
                            #         baseAssetPrecision = symbol['baseAssetPrecision']
                            #         quotePrecision = symbol['quotePrecision']

                            #         if symbol['symbol'] == sigdata['Coin']:
                            #             minPrice = symbol['filters'][0]['minPrice']
                            #             minQty = symbol['filters'][2]['minQty']

                            #             precisionqty = str(minQty).find('1')
                            #             precisionprice = str(minPrice).find('1')
                            #             pqty = precisionqty - 1
                            #             pprice = precisionprice - 1

                            #     amount = qty
                            #     precision = int(pqty)
                            #     amt_str = "{:0.0{}f}".format(amount, precision)

                            #     amount2 = penew
                            #     precision2 = int(pprice)
                            #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                            #     print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                            cursor1.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Bajo",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection1.commit()
                            mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='mlm', host='127.0.0.1',
                                                                  port='3306')

                            cursor2 = mariadb_connection2.cursor()
                            cursor2.execute(
                                "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                ("🟢 Compra", tp, sl, dateup,
                                 "Bajo",
                                 penew, "Abierta", sigdata['Coin'], hourup))
                            mariadb_connection2.commit()
                            for x in range(len(dfuser)):

                                usertype = dfuser['type'][countid]

                                if usertype == "free":
                                    bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                    response = requests.get(send_text)
                                    print(response.json())
                                if usertype == "prem":
                                    bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                        'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                        "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                    bot_chatID = str(dfuser['chatid'][countid])
                                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                    response = requests.get(send_text)
                                    print(response.json())

                                countid = countid + 1


                    except BinanceAPIException as e:
                        print(e.status_code)
                        print(e.message)
                        client = Client(api_key, api_secret)


                # bot_messagefull = "₿ Par" + sigdata[
                #     'Coin'] + '⚠⚠\n ➕ BBRSI {} \n ➕ EMARSI {} \n ➕ BINDHAST {} \n ➕ EMARSICCI {}\n ➕ ADXMOMENTUM {}\n ➕ ADXSMAS {}'.format(
                #     sigdata['BBRSI'], sigdata['EMARSI'], sigdata['BINDHAST'], sigdata['EMARSICCI'], sigdata['ADXMOMENTUM'],
                #     sigdata['ADXSMAS'])


        if (timeactualsecondsnew <= timeactsecondsnew) and (timeactualsecondsnew >= time4new):
            print('Estamos recopilando datos \n Wait please \n wait please')

            # best[1] = "d"

            # best["Added values"] = best[0].add(list)
            #print(best.index)

        else:
            print('Actualizando twitter')
            if len(listmov.index) > 0:

                for index, sigdata in pd.DataFrame(listpro).iterrows():

                    coin_name = sigdata['Coin']
                    

                    if (sigdata == "🔴 Venta").sum() > 0 and (sigdata == "🟢 Compra").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            sl = pe + (pe * 0.01)
                            tp = pe - (pe * 0.02)

                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')

                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0

                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False
                            else:
                                verify = True
                            cursor1 = mariadb_connection1.cursor()

                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Alto",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()

                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Alto",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()

                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                            "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1

                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)
                            client = Client(api_key, api_secret)

                    if (sigdata == "🟢 Compra").sum() > 0 and (sigdata == "🔴 Venta").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            penew = pe - (pe * 0.005)
                            sl = penew - (penew * 0.02)
                            tp = penew + (penew * 0.02)
                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')
                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            cursor1 = mariadb_connection1.cursor()

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False

                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                                # balance = client.get_asset_balance(asset='BTC')

                                # print(balance['free'])

                                # if float(balance['free']) > 0:

                                #     qty = float(balance['free']) / float(penew)

                                #     exch = client.get_exchange_info()
                                #     pqty = 0
                                #     pprice = 0

                                #     for symbol in exch['symbols']:
                                #         baseAssetPrecision = symbol['baseAssetPrecision']
                                #         quotePrecision = symbol['quotePrecision']

                                #         if symbol['symbol'] == sigdata['Coin']:
                                #             minPrice = symbol['filters'][0]['minPrice']
                                #             minQty = symbol['filters'][2]['minQty']

                                #             precisionqty = str(minQty).find('1')
                                #             precisionprice = str(minPrice).find('1')
                                #             pqty = precisionqty - 1
                                #             pprice = precisionprice - 1

                                #     amount = qty
                                #     precision = int(pqty)
                                #     amt_str = "{:0.0{}f}".format(amount, precision)

                                #     amount2 = penew
                                #     precision2 = int(pprice)
                                #     amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                                #     print(amt_str)

                                    #try:
                                    #    buy_order_limit = client.create_order(
                                    #        symbol=sigdata['Coin'],
                                    #        side='BUY',
                                    #        type='LIMIT',
                                    #        timeInForce='GTC',
                                    #        quantity=float(amt_str),
                                    #        price=amt_str2)
                                    #    print(buy_order_limit)
                                        # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                        # print(order)
                                    #except BinanceAPIException as e:
                                    #    print(e.status_code)
                                    #    print(e.message)

                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Alto",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()
                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Alto",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()
                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Alto'.format(
                                            "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1


                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)

                    if (sigdata == "🔴 Venta").sum() > 1 and (sigdata == "🟢 Compra").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            sl = pe + (pe * 0.01)
                            tp = pe - (pe * 0.02)

                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')

                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            cursor1 = mariadb_connection1.cursor()

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False
                            else:
                                verify = True
                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Medio",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()
                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Alto",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()
                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                            "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1

                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)
                            client = Client(api_key, api_secret)

                    if (sigdata == "🟢 Compra").sum() > 1 and (sigdata == "🔴 Venta").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            penew = pe - (pe * 0.005)
                            sl = penew - (penew * 0.02)
                            tp = penew + (penew * 0.02)
                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')
                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            cursor1 = mariadb_connection1.cursor()

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False

                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                                # balance = client.get_asset_balance(asset='BTC')

                                # qty = float(balance['free']) / float(penew)

                                # exch = client.get_exchange_info()
                                # pqty = 0
                                # pprice = 0

                                # for symbol in exch['symbols']:
                                #     baseAssetPrecision = symbol['baseAssetPrecision']
                                #     quotePrecision = symbol['quotePrecision']

                                #     if symbol['symbol'] == sigdata['Coin']:
                                #         minPrice = symbol['filters'][0]['minPrice']
                                #         minQty = symbol['filters'][2]['minQty']

                                #         precisionqty = str(minQty).find('1')
                                #         precisionprice = str(minPrice).find('1')
                                #         pqty = precisionqty - 1
                                #         pprice = precisionprice - 1

                                # amount = qty
                                # precision = int(pqty)
                                # amt_str = "{:0.0{}f}".format(amount, precision)

                                # amount2 = penew
                                # precision2 = int(pprice)
                                # amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                                # print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Medio",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()
                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Alto",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()
                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Medio'.format(
                                            "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1


                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)
                            client = Client(api_key, api_secret)
                    if (sigdata == "🔴 Venta").sum() > 2 and (sigdata == "🟢 Compra").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            sl = pe + (pe * 0.01)
                            tp = pe - (pe * 0.02)

                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')

                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            cursor1 = mariadb_connection1.cursor()

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False
                            else:
                                verify = True
                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Bajo",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()
                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🔴 Venta", tp, sl, dateup,
                                     "Alto",
                                     pe, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()
                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Venta " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                            "%.8f" % float(pe), "%.8f" % float(tp), "%.8f" % (sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1

                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)
                            client = Client(api_key, api_secret)

                    if (sigdata == "🟢 Compra").sum() > 2 and (sigdata == "🔴 Venta").sum() == 0:
                        try:
                            current_datetime = datetime.datetime.now()

                            # Set the start time to 12:00 AM (00:00:00) 7 days ago
                            start_datetime = current_datetime - datetime.timedelta(days=1)
                            start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

                            # Set the end time to the current date and time
                            end_datetime = current_datetime

                            # Convert the datetime objects to timestamps in milliseconds
                            start_timestamp = int(start_datetime.timestamp() * 1000)
                            end_timestamp = int(end_datetime.timestamp() * 1000)
                            kline_url = f'https://api.bybit.com/derivatives/v3/public/kline?category=linear&symbol={coin_name}&interval=15&start={start_timestamp}&end={end_timestamp}'
                            kline_response = requests.get(kline_url)
                            kline_data = kline_response.json()
                            #print(kline_data['result']['list'])
                            #df2 = pd.DataFrame(kline_data['result']['list'], columns=['Open time','s','sn' 'Close', 'High', 'Low', 'Open', 'Volume'])
                            df2 = pd.DataFrame(kline_data['result']['list'])
                            df2['Open time'] = pd.to_datetime(df2[0], unit='ms')
                            df2.set_index('Open time', inplace=True)
                            df2['Close'] = df2[4].astype(float)
                            df2['High'] = df2[2].astype(float)
                            df2['Low'] = df2[3].astype(float)
                            df2['Open'] = df2[1].astype(float)
                            print(df2['Close'].iloc[-1])
                            pe = float(df2['Close'].iloc[-1])
                            # print(pe)
                            penew = pe - (pe * 0.005)
                            sl = penew - (penew * 0.02)
                            tp = penew + (penew * 0.01)
                            bot_token = '1874646538:AAHB8ZGWT6rPO8GX5GGiHDStemesb8jme_o'
                            # bot_chatID = '-1101441080121'
                            mariadb_connection1 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                  database='agarjoya_bitpattern', host='127.0.0.1',
                                                                  port='3306')
                            query = "SELECT chatid, type FROM users;"
                            dfuser = pd.read_sql_query(query, mariadb_connection1)
                            countid = 0
                            IST = pytz.timezone('America/Bogota')
                            e = datetime.datetime.now(IST)

                            hours = getattr(e, 'hour')
                            minutes = getattr(e, 'minute')
                            second = getattr(e, 'second')
                            days = getattr(e, 'day')
                            month = getattr(e, 'month')
                            year = getattr(e, 'year')

                            dateup = str(year) + "-" + str(month) + "-" + str(days)
                            hourup = str(hours) + ":" + str(minutes) + ":" + str(second)

                            query2 = "SELECT coin type FROM signals WHERE coin='{}' and date='{}' and status='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsig = pd.read_sql_query(query2, mariadb_connection1)

                            cursor1 = mariadb_connection1.cursor()

                            query3 = "SELECT coin,type, hour FROM signals WHERE coin='{}' and date='{}' and status!='Abierta';".format(
                                sigdata['Coin'], dateup)
                            dfsigver = pd.read_sql_query(query3, mariadb_connection1)
                            verify = False

                            if len(dfsigver) > 0:
                                hour = dfsigver['hour'].iloc[-1]
                                print('Hora pedido:', (hour))
                                time2 = pd.to_timedelta(hour)

                                # Tiempo seleccionado + 1 hs
                                time3 = pd.Timedelta(time2)
                                time4 = time3.total_seconds()
                                print('hora actualizaci0n:', (time4))
                                hoursd = (time4 // 3600) + 4
                                minutesd = (time4 % 3600) // 60
                                secondsd = time4 % 60
                                timeact = timedelta(hours=hoursd, minutes=minutesd, seconds=secondsd)
                                timeactdelta = pd.Timedelta(timeact)
                                timeactseconds = timeactdelta.total_seconds()

                                print('Hora vencimiento:', (timeactseconds))
                                d = datetime.datetime.now()

                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)
                                print(e)

                                hoursact = getattr(e, 'hour')
                                minutesact = getattr(e, 'minute')
                                secondsact = getattr(e, 'second')

                                timeactual = timedelta(hours=hoursact, minutes=minutesact, seconds=secondsact)
                                timeactualdelta = pd.Timedelta(timeactual)
                                timeactualseconds = timeactualdelta.total_seconds()
                                if timeactualseconds >= timeactseconds:
                                    verify = True
                                else:
                                    verify = False

                            if len(dfsig) == 0 and verify == True:
                                IST = pytz.timezone('America/Bogota')
                                e = datetime.datetime.now(IST)

                                hours = getattr(e, 'hour')
                                minutes = getattr(e, 'minute')
                                second = getattr(e, 'second')
                                days = getattr(e, 'day')
                                month = getattr(e, 'month')
                                year = getattr(e, 'year')

                                dateup = str(year) + "-" + str(month) + "-" + str(days)
                                hourup = str(hours) + ":" + str(minutes) + ":" + str(second)
                                # balance = client.get_asset_balance(asset='BTC')

                                # qty = float(balance['free']) / float(penew)

                                # exch = client.get_exchange_info()
                                # pqty = 0
                                # pprice = 0

                                # for symbol in exch['symbols']:
                                #     baseAssetPrecision = symbol['baseAssetPrecision']
                                #     quotePrecision = symbol['quotePrecision']

                                #     if symbol['symbol'] == sigdata['Coin']:
                                #         minPrice = symbol['filters'][0]['minPrice']
                                #         minQty = symbol['filters'][2]['minQty']

                                #         precisionqty = str(minQty).find('1')
                                #         precisionprice = str(minPrice).find('1')
                                #         pqty = precisionqty - 1
                                #         pprice = precisionprice - 1

                                # amount = qty
                                # precision = int(pqty)
                                # amt_str = "{:0.0{}f}".format(amount, precision)

                                # amount2 = penew
                                # precision2 = int(pprice)
                                # amt_str2 = "{:0.0{}f}".format(amount2, precision2)

                                # print(amt_str)

                                #try:
                                #    buy_order_limit = client.create_order(
                                #        symbol=sigdata['Coin'],
                                #        side='BUY',
                                #        type='LIMIT',
                                #        timeInForce='GTC',
                                #        quantity=float(amt_str),
                                #        price=amt_str2)
                                #    print(buy_order_limit)
                                    # order = client.create_order(symbol=sigdata['Coin'], side='BUY', type='MARKET', quantity=float(amt_str))
                                    # print(order)
                                #except BinanceAPIException as e:
                                #    print(e.status_code)
                                #    print(e.message)
                                cursor1.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Bajo",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection1.commit()
                                mariadb_connection2 = mariadb.connect(user='dev', password='bMAWdCCCpS@7',
                                                                      database='mlm', host='127.0.0.1',
                                                                      port='3306')

                                cursor2 = mariadb_connection2.cursor()
                                cursor2.execute(
                                    "INSERT INTO signals (type,tp,sl,date,riesgo,price,status,coin,hour) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                    ("🟢 Compra", tp, sl, dateup,
                                     "Alto",
                                     penew, "Abierta", sigdata['Coin'], hourup))
                                mariadb_connection2.commit()
                                for x in range(len(dfuser)):

                                    usertype = dfuser['type'][countid]

                                    if usertype == "free":
                                        bot_message = "Actualiza tu plan a premium para recibir mejores señales"
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                                        response = requests.get(send_text)
                                        print(response.json())
                                    if usertype == "prem":
                                        bot_messagefull = "₿ Prueba de Señal Compra " + sigdata[
                                            'Coin'] + ' ⚠⚠ \n ➕ Punto Entrada : {} \n ➕ Toma Ganan: {} \n ➕ Perdida {} \n ➕ Riesgo: Bajo'.format(
                                            "%.8f" % float(penew), "%.8f" % float(tp), "%.8f" % float(sl))
                                        bot_chatID = str(dfuser['chatid'][countid])
                                        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_messagefull
                                        response = requests.get(send_text)
                                        print(response.json())

                                    countid = countid + 1


                        except BinanceAPIException as e:
                            print(e.status_code)
                            print(e.message)
                            client = Client(api_key, api_secret)
            # send_twit = best.to_string()
            # s = Template('🔝 Analisis 🔝 \n #Binance \n $what \n Info #crypto https://t.me/bitsolution_bot')
            # send_twit = s.substitute(what=pd.DataFrame(listpro).iloc[0:4,0:4].to_string(index=False))
            # s2 = Template('🔝 Analisis Tecnico 🔝 \n Revisa nuestros planes de inversion \n $what')
            # send_twit2 = s2.substitute(what=pd.DataFrame(listpro).iloc[0:5,0:4].to_string(index=False,))
            # send_twit2full = s2.substitute(what=pd.DataFrame(listpro).to_string(index=False, ))
            #print(send_twit2)
            # print(api.VerifyCredentials())
            listmov = pd.DataFrame(listpro)
            print(len(listmov.index))

            if len(listmov.index) > 0:
                telegram_bot_sendtext(listpro,listpro2)
                #status = api.PostUpdate(send_twit)

            # Tiempo actualizar
            valor3 = strftime("%H:%M:%S", gmtime())
            count3 = 1
            cursor.execute("""UPDATE topcoinsu SET twitter_time1 = %s WHERE coin_id = %s""", (timeactualn, count3))
            mariadb_connection.commit()
        mariadb_connection.close()
        sleep(5)







