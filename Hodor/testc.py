import os
coin_name = 'APT'
command = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot.py {}'.format(coin_name.replace('USDT','') + "/USDT")
os.system(f'start cmd /c "{command}"')
command2 = 'python3 /home/ec2-user/Desktop/Pattern/bybytbot2.py {}'.format(coin_name.replace('USDT','')  + "/USDT")
os.system(f'start cmd /c "{command2}"')