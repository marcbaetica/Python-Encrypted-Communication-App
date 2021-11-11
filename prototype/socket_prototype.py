import subprocess
from pprintpp import pprint
from time import sleep


subprocess.Popen('python server.py', shell=True)
subprocess.run('python client.py', shell=True)
