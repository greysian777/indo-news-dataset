import os 
from datetime import datetime

today = datetime.now().strftime('[COLAB] generated at %H:%M:%S')
os.system("git add .")
os.system(f"git commit -m \'{today}\'")
print(today)
os.system('git push colab lab')

print('manjiw!')