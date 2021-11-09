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


class ServerSocket:
    def __init__(self, ip_address, max_connections):
        self.ip_address = ip_address
        self.port = SOCKET_PORT
        self.max_connections = max_connections
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self.handler_sockets = []
        self._bind_to_host(self.ip_address)  # TODO: socket.gethostname() to broadcast each others' ip
        self._set_max_connect_requests(self.max_connections)
        self.handler_sockets.append(self._accept_connection())  # TODO: Notify client has established socket connection.
        self._handle_incoming_data()

    def _bind_to_host(self, ip_address):
        self.socket.bind((ip_address, self.port))

    def _set_max_connect_requests(self, count):
        self.socket.listen(count)

    def _accept_connection(self):
        print(f'Server is listening on {self.ip_address}:{self.port}.'
              f' Max incoming connections set to {self.max_connections}.')
        return self.socket.accept()

    def _handle_incoming_data(self):
        handler_socket, client_addr = self.handler_sockets[0]  # Maybe not a great idea to have it as a list.
        # TODO: toggle between send / receive.
        while True:
            data_received = CommsProtocolHandler.receive_data_attempt(handler_socket, 'Server')
            if not CommsProtocolHandler.is_other_party_socket_closed(data_received, handler_socket.getpeername(), 'Server'):
                print(f'[Server] Received message: {data_received}')
            else:
                handler_socket.close()
                break
            data_to_send = input(f'[Server] Data to send ({EXIT_CODE} to close connection): ')
            if not CommsProtocolHandler.is_close_socket_attempt(data_to_send, handler_socket.getpeername(), 'Server'):
                print(handler_socket)
                CommsProtocolHandler.send_data_attempt(handler_socket, data_to_send)
            else:
                handler_socket.close()
                break
