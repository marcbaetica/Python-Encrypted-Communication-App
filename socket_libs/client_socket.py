import socket
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
IP_TO_CONNECT_TO = 'localhost'
SOCKET_PORT = 50000


class ClientSocket:
    def __init__(self):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)

    def connect(self):
        self.socket.connect((IP_TO_CONNECT_TO, SOCKET_PORT))

    def send_data(self, data):  # TODO: Make data the one that says something.
        self.socket.send(encode_and_apply_padding(data, 10))  # TODO: 10 must be env variable.

    def receive_data(self):
        data = self.socket.recv(1024).decode()  # TODO: Size has to be adjustable. Maybe parametrize or ser as env var?
        print(f'Client received message: "{data}"')
