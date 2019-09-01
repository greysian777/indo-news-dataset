import subprocess

if __name__=="__main__": 
    while True: 
        p = subprocess.Popen('python parallel_kompas.py', shell=True)
        p.wait()