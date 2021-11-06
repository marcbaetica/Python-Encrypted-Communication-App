import socket
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
SERVER_SOCKET_PORT = 50000


class ServerSocket:
    def __init__(self, ip_address, max_connections):
        self.ip_address = ip_address
        self.port = SERVER_SOCKET_PORT
        self.max_connections = max_connections
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self.handler_sockets = []
        self._bind_to_host(self.ip_address)
        self._set_max_connect_requests(self.max_connections)
        self.handler_sockets.append(self._accept_connection())
        self._handle_incoming_data()

    def _bind_to_host(self, ip_address):
        self.socket.bind((ip_address, SERVER_SOCKET_PORT))

    def _set_max_connect_requests(self, count):
        self.socket.listen(count)

    def _accept_connection(self):
        print(f'Server is listening on {self.ip_address}:{self.port}.'
              f' Max incoming connections set to {self.max_connections}.')
        return self.socket.accept()

    def _handle_incoming_data(self):
        handler_s, client_addr = self.handler_sockets[0]  # Maybe not a great idea to have it as a list.
        incoming_payload_size = 10  # TODO: Env variable.
        actual_recv_chars = 0
        # TODO: Infinite loop here!
        incoming_payload_size = decode_and_remove_padding(handler_s.recv(incoming_payload_size))
        print(f'Server received size of next message from client {client_addr[0]}:{client_addr[1]}: "{incoming_payload_size}"')
        if incoming_payload_size:
            handler_s.send(b'OK')  # TODO: Cleaner encoding.
            data = handler_s.recv(incoming_payload_size).decode()
            print(f'Server received message from client {client_addr[0]}:{client_addr[1]}: "{data}"')
            handler_s.send(b'We heard you loud and clear. Server handler out!')  # TODO: Cleaner encoding.
        # # handler_s.close()  # Might be problematic closing prematurely?