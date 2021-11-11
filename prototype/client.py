import socket
import threading
from time import sleep


print('Hello from the client!')

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(('localhost', 50000))

print(f'[Client] Client socket started: {c}')


def receive_incoming_data():
    while True:
        sleep(1)
        data = c.recv(10)
        print(f'[Client] Client received message: {data}')


x = threading.Thread(target=receive_incoming_data, daemon=True)
x.start()


message = ''
while message != 'ok':
    message = input('Insert new message: \n')
    print(message)
