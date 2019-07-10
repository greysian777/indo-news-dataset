import os 
import time

os.system('python3 pusher.py')

for _ in range(5):
    time.sleep(3600)
    os.system('python3 pusher.py')
    print(f'hour {_}')