import os 
from datetime import datetime

today = datetime.now().strftime('generated at %H:%M:%S from labilkom')
os.system("git add .")
os.system(f"git commit -m \"{today}\"")
print(today)
os.system('git push origin lab')

print('manjiw!')