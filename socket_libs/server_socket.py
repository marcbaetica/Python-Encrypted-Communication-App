import os
import socket
from dotenv import load_dotenv
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


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
        data = ServerSocket._receive_data(handler_s)
        print(f'Server received message: "{data}"')
        # Ending connection.
        ServerSocket._send_data(handler_s, 'Roger. We heard you loud and clear. Server handler out!')
        handler_s.close()

    @staticmethod
    def _receive_confirmation(handler_socket):
        confirmation = handler_socket.recv(len(CONFIRMATION_CODE)).decode()
        return True if confirmation == CONFIRMATION_CODE else False

    @staticmethod
    def _receive_data(handler_socket):
        incoming_payload_length = decode_and_remove_padding(handler_socket.recv(PADDED_MESSAGE_SIZE))
        print(f'Server received size of next message: "{incoming_payload_length}"')
        handler_socket.send(CONFIRMATION_CODE.encode())
        payload = handler_socket.recv(incoming_payload_length).decode()
        return payload

    @staticmethod
    def _send_data(handler_socket, payload):
        outgoing_payload_length = len(payload) + 3  # Accounts for b'' characters that will also be amended.
        handler_socket.send(encode_and_apply_padding(outgoing_payload_length, PADDED_MESSAGE_SIZE))
        confirmation = ServerSocket._receive_confirmation(handler_socket)  # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
        if confirmation:
            handler_socket.send(payload.encode())
        else:
            # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
            pass

# TODO: _receive_data and _send_data from Server and Client sockets has a lot of overlap. Probably best fitted in a common library.
