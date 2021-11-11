import socket
from time import sleep


print('Hello from the server!')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
h_socket, c_addr = s.accept()

print(f'[Server] Connected to {c_addr} via {h_socket}')

sleep(3)

for _ in range(10):
    h_socket.send(b'SSSSSSSSSS')

h_socket.close()

