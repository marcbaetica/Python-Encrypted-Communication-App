import socket


SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
IP_TO_CONNECT_TO = 'localhost'
SOCKET_PORT = 50000


class ClientSocket:
    def __init__(self):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)

    def connect(self):
        self.socket.connect((IP_TO_CONNECT_TO, SOCKET_PORT))

    def send_data(self, data):  # TODO: make data the one that says something.
        self.socket.send(data)

    def receive_data(self):
        data = self.socket.recv(1024)
        print(f'The server replied with message: {data}')
