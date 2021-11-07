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


class ClientSocket:
    def __init__(self, ip_address):
        self.socket = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self._connect(ip_address)

    def _connect(self, ip_address):
        self.socket.connect((ip_address, SOCKET_PORT))

    def _receive_confirmation(self):
        confirmation = self.socket.recv(len(CONFIRMATION_CODE))
        return True if confirmation == CONFIRMATION_CODE.encode() else False

    def send_data_attempt(self, payload):
        outgoing_payload_length = len(payload) + 3  # Accounts for b'' characters that will also be amended.
        self.socket.send(encode_and_apply_padding(outgoing_payload_length, PADDED_MESSAGE_SIZE))
        confirmation = self._receive_confirmation()  # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
        if confirmation:
            self.socket.send(payload.encode())
        else:
            # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
            pass

    def receive_data_attempt(self):
        data = self._receive_data()  # TODO: Try/except block + Handle error cases... dropped signal, collisions, reconfirm, etc.
        print(f'Client received message: {data}')

    def _receive_data(self):
        incoming_payload_length = decode_and_remove_padding(self.socket.recv(PADDED_MESSAGE_SIZE))
        print(f'Client received size of next message: "{incoming_payload_length}"')
        self.socket.send(CONFIRMATION_CODE.encode())
        payload = self.socket.recv(incoming_payload_length).decode()
        return payload

# TODO: _receive_data and send_data_attempt from Server and Client sockets has a lot of overlap. Probably best fitted in a common library.
