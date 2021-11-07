import socket
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
SOCKET_PORT = 50000
CONFIRMATION_CODE = 'OK'


class ClientSocket:
    def __init__(self, ip_address):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self._connect(ip_address)

    def _connect(self, ip_address):
        self.socket.connect((ip_address, SOCKET_PORT))

    def _receive_confirmation(self):
        confirmation = self.receive_data(2)
        return True if confirmation == CONFIRMATION_CODE else False

    def send_data_attempt(self, payload):  # TODO: Make data the one that says something.
        payload = payload.encode()
        payload_length = len(payload) + 3  # Accounts for b'' characters that will also be sent.
        self.socket.send(encode_and_apply_padding(payload_length, 10))  # TODO: 10 must be env variable.
        confirmation = self._receive_confirmation()  # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
        if confirmation:
            self.socket.send(payload)
        else:
            # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
            pass

    def receive_data(self, incoming_payload_size):
        data = self.socket.recv(incoming_payload_size).decode()  # TODO: Size has to be adjustable. Maybe parametrize or ser as env var?
        print(f'Client received message: "{data}"')
        return data
