import os
import socket
from dotenv import load_dotenv
from lib.chat_handler import ChatHandler


load_dotenv()

SOCKET_FAMILY = eval(os.getenv('SOCKET_FAMILY'))
SOCKET_TYPE = eval(os.getenv('SOCKET_TYPE'))
SOCKET_PORT = int(os.getenv('SOCKET_PORT'))
PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
EXIT_CODE = os.getenv('EXIT_CODE')


class ClientSocket:
    def __init__(self, ip_address):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self._connect(ip_address)
        self._handle_chat()

    def _connect(self, ip_address):
        self.socket.connect((ip_address, SOCKET_PORT))

    def _handle_chat(self):
        ChatHandler(self.socket, 'Client').handle_chat()

    def close(self):
        self.socket.close()
