import subprocess


subprocess.run("dir", shell=True)
subprocess.run("python --version", shell=True)
subprocess.Popen("python server.py", shell=True)
subprocess.run(" python client.py", shell=True)