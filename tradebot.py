import asyncio
import copy
import json
import logging
import math
import os
import time
from time import gmtime, strftime
from random import SystemRandom
import binarycom
from neural_network.evaluation import classify
from utils.image_convertor import save_image


async def main():
    loop = asyncio.get_running_loop()
    if not os.path.isdir('images'):
        os.mkdir('images')
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    # logging
    logging.basicConfig(filename=f'logs/aa.log',
                        filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y::%H:%M:%S')

    with open('configuration.json', mode='r') as configuration_file:
        configuration = json.load(configuration_file)
    websocket = await binarycom.connect(configuration['app_id'])
    print('Iniciar sesión en Binary...')
    await binarycom.authorize(websocket, configuration['api_token'])
    print('ОК')
    steps = configuration['steps']
    parameters = copy.deepcopy(configuration['parameters'])
    parameters['amount'] = configuration['base_bet']
    parameters['duration'] = configuration['chart_length'] * configuration['y'] * 60
    parameters['duration_unit'] = 's'
    parameters['currency'] = 'USD'
    total_income = 0
    while True:
        to = math.floor(time.time())
        tick_history = await binarycom.tick_history(websocket, parameters['symbol'],
                                                    to - configuration['chart_length'] * 60, to)
        longitud = 8

        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        cryptogen = SystemRandom()

        p = ""

        while longitud > 0:
            p = p + cryptogen.choice(valores)

            longitud = longitud - 1

        imgid = p
        name = "imgs"

        save_image(tick_history['history']['prices'], 'images', f'{name}.png')
        class_ = classify(f'images/{name}.png')

        print(class_)

        if class_ == 0:
            await loop.run_in_executor(None, logging.info, f'Image: {name}, result: Horario inadecuado')
            print('Mal horario. Esperar...')
            await asyncio.sleep(configuration['wait'] * 5)
            continue
        if class_ == 1:
            print('Gráfico de disminución de precio.')
            parameters['contract_type'] = 'PUT'
            #parameters['barrier'] = - configuration['barrier']
            message = 'Tabla descendente'

        else:
            print('Gráfico de aumento de precio.')
            parameters['contract_type'] = 'CALL'
            #parameters['barrier'] = configuration['barrier']
            message = 'Horario ascendente'
        await loop.run_in_executor(None, logging.info, f'Image:{name}, result: {message}')

        while True:
            to = math.floor(time.time())
            tick_history = await binarycom.tick_history(websocket, parameters['symbol'],
                                                        to - configuration['chart_length'] * 60, to)
            longitud = 8

            valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

            cryptogen = SystemRandom()

            p = ""

            while longitud > 0:
                p = p + cryptogen.choice(valores)

                longitud = longitud - 1

            imgid = p
            name = "imgs"

            save_image(tick_history['history']['prices'], 'images', f'{name}.png')
            class_ = classify(f'images/{name}.png')

            print(class_)

            if class_ == 0:
                await loop.run_in_executor(None, logging.info, f'Image: {name}, result: Horario inadecuado')
                print('Mal horario. Esperar...')
                await asyncio.sleep(configuration['wait'] * 5)
                continue
            if class_ == 1:
                print('Gráfico de disminución de precio.')
                parameters['contract_type'] = 'PUT'
                # parameters['barrier'] = - configuration['barrier']
                message = 'Tabla descendente'

            else:
                print('Gráfico de aumento de precio.')
                parameters['contract_type'] = 'CALL'
                # parameters['barrier'] = configuration['barrier']
                message = 'Horario ascendente'
            await loop.run_in_executor(None, logging.info, f'Image:{name}, result: {message}')
            print('Comprar...')
            balance_before_buy = await binarycom.balance(websocket)
            print(balance_before_buy)
            resultct = await binarycom.buy_contract(websocket, parameters)
            print(resultct)
            await asyncio.sleep(parameters['duration'] + 2)
            balance_after_buy = await binarycom.balance(websocket)
            income = balance_after_buy['balance']['balance'] - balance_before_buy['balance']['balance']
            print(f'Lucro: {income}')
            total_income = total_income + income
            print(f'Beneficio total: {total_income}')

            await loop.run_in_executor(None, logging.info,
                                       f"Saldo antes de la compra: {balance_before_buy['balance']['balance']},"
                                       f"saldo después de la compra: {balance_after_buy['balance']['balance']}"
                                       f"Ingresos de la última apuesta: {income}, ingresos totales para la autorización actual: {total_income}"
                                       f"Paso: {steps}, monto de la apuesta actual: {parameters['amount']}"
                                       )
            riesgo = parameters['amount'] + income
            if income < 0:
                await asyncio.sleep(configuration['pause'] * 60)
                if steps > 0:
                    print('Duplicando mi apuesta...')
                    parameters['amount'] = parameters['amount'] * 2
                    steps = steps - 1

                ##                if steps == 0 and riesgo == 0:
                ##                    await loop.run_in_executor(None, logging.info,f'Estoy empezando de nuevo. Tasa inicial: {configuration["base_bet"]}')
                ##                    print('Yo establezco la tarifa base...')
                ##                    parameters['amount'] = configuration['base_bet']
                ##                    steps = configuration['steps']
                ##                    await asyncio.sleep(configuration['pause'] * 60)

                break
            else:
                await loop.run_in_executor(None, logging.info,
                                           f'Estoy empezando de nuevo. Tasa inicial: {configuration["base_bet"]}')
                print('Yo establezco la tarifa base...')
                parameters['amount'] = configuration['base_bet']
                steps = configuration['steps']

    await websocket.close()


asyncio.run(main())