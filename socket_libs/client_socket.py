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
EXIT_CODE = os.getenv('EXIT_CODE')


class ClientSocket:
    def __init__(self, ip_address):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self._connect(ip_address)
        self._handle_chat()

    def _connect(self, ip_address):
        self.socket.connect((ip_address, SOCKET_PORT))

    def _handle_chat(self):
        while True:
            data_to_send = input(f'[Client] Data to send ({EXIT_CODE} to close connection): ')
            if not CommsProtocolHandler.is_close_socket_attempt(data_to_send, self.socket.getsockname()):
                self.send_data_attempt(data_to_send)
            else:
                self.socket.close()
                break
            data_received = self.receive_data_attempt()
            if not CommsProtocolHandler.is_other_party_socket_closed(data_received, self.socket.getsockname()):
                print(f'[Client] Received message: {data_received}')
            else:
                self.socket.close()
                break

    def send_data_attempt(self, payload):
        CommsProtocolHandler.send_data(self.socket, payload)  # TODO: handle exceptions here.

    def receive_data_attempt(self):
        return CommsProtocolHandler.receive_data(self.socket, 'Client')  # TODO: handle exceptions here.

    def close(self):
        self.socket.close()
