import os 
from datetime import datetime

today = datetime.now().strftime('generated at %H:%M:%S from collab')
os.system("git add .")
os.system(f"git commit -m '{today}'")
print(today)
os.system('git push colab lab')

print('manjiw!')