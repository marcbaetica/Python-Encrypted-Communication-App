import os
import socket
from dotenv import load_dotenv
from lib.comms_protocol import CommsProtocolHandler


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
        # TODO: toggle between send / receive.
        while True:
            try:
                data_to_send = ''
                while data_to_send == '':  # Empty payloads are synonymous to connection closing.
                    data_to_send = input(f'[Client] Data to send ({EXIT_CODE} to close connection): ')
                if not CommsProtocolHandler.is_close_socket_attempt(data_to_send, self.socket.getpeername(), 'Client'):
                    print(self.socket)
                    CommsProtocolHandler.send_data_attempt(self.socket, data_to_send)
                else:
                    self.socket.close()
                    break
                data_received = CommsProtocolHandler.receive_data_attempt(self.socket, 'Client')
                if not CommsProtocolHandler.is_other_party_socket_closed(data_received, self.socket.getpeername(), 'Client'):
                    print(f'[Client] Received message: {data_received}')
                else:
                    self.socket.close()
                    break
            except OSError as e:
                # When socket has been terminated, all subsequent operations involving the object should simply break.
                # Specific scenario logging has been accounted for.
                # OSError: [WinError 10038] An operation was attempted on something that is not a socket
                break

    def close(self):
        self.socket.close()
