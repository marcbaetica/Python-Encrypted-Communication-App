import socket


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
        for handler_s, client_addr in self.handler_sockets:
            while True:
                data = handler_s.recv(1024)  # TODO: fix bug -> make non-blocking or send size first
                print(data)
                if not data:
                    handler_s.send(b'We heard you loud and clear. Server handler out!')
                    handler_s.close()
                    break  # breaks out of for loop as well?
                print(f'Server received {data} from client at {client_addr[0]}:{client_addr[1]}')
