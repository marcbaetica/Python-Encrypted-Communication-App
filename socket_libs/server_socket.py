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


class ServerSocket:
    def __init__(self, ip_address, max_connections):
        self.ip_address = ip_address
        self.port = SOCKET_PORT
        self.max_connections = max_connections
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self.handler_sockets = []
        self._bind_to_host(self.ip_address)
        self._set_max_connect_requests(self.max_connections)
        self.handler_sockets.append(self._accept_connection())
        self._handle_incoming_data()

    def _bind_to_host(self, ip_address):
        self.socket.bind((ip_address, self.port))

    def _set_max_connect_requests(self, count):
        self.socket.listen(count)

    def _accept_connection(self):
        print(f'Server is listening on {self.ip_address}:{self.port}.'
              f' Max incoming connections set to {self.max_connections}.')
        return self.socket.accept()

    def _handle_incoming_data(self):  # TODO: Logical operation ServerSocker._handle_incoming_data is not accurate.
        handler_s, client_addr = self.handler_sockets[0]  # Maybe not a great idea to have it as a list.
        # TODO: Infinite loop here!
        data = ServerSocket._receive_data_attempt(handler_s)
        print(f'Server received message: "{data}"')
        # Ending connection.
        ServerSocket._send_data_attempt(handler_s, 'Roger. We heard you loud and clear. Server handler out!')
        handler_s.close()

    @staticmethod
    def _receive_data_attempt(handler_socket):
        # TODO: Try/except block + Handle error cases... dropped signal, collisions, reconfirm, etc.
        payload = CommsProtocolHandler.receive_data(handler_socket)
        return payload

    @staticmethod
    def _send_data_attempt(handler_socket, payload):
        # TODO: Try/except block + Handle error cases... dropped signal, collisions, reconfirm, etc.
        CommsProtocolHandler.send_data(handler_socket, payload)
