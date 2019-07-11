import os 
import time

os.system('python pusher.py')

for _ in range(5):
    time.sleep(3600)
    os.system('python pusher.py')
    print(f'hour {_+1}')