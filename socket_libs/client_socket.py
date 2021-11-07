import os
import socket
from dotenv import load_dotenv
from lib.comms_protocol import CommsProtocolHandler


load_dotenv()

SOCKET_FAMILY = eval(os.getenv('SOCKET_FAMILY'))
SOCKET_TYPE = eval(os.getenv('SOCKET_TYPE'))
SOCKET_PORT = int(os.getenv('SOCKET_PORT'))
PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
CONFIRMATION_CODE = os.getenv('CONFIRMATION_CODE')


class ClientSocket:
    def __init__(self, ip_address):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self._connect(ip_address)

    def _connect(self, ip_address):
        self.socket.connect((ip_address, SOCKET_PORT))

    def send_data_attempt(self, payload):
        # TODO: Try/except block + Handle error cases... dropped signal, collisions, reconfirm, etc.
        CommsProtocolHandler.send_data(self.socket, payload)

    def receive_data_attempt(self):
        # TODO: Try/except block + Handle error cases... dropped signal, collisions, reconfirm, etc.
        data = CommsProtocolHandler.receive_data(self.socket)
        print(f'Client received message: {data}')
