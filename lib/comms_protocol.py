import os
from dotenv import load_dotenv
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


load_dotenv()

PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
CONFIRMATION_CODE = os.getenv('CONFIRMATION_CODE')


class CommsProtocolHandler:

    @classmethod
    def send_data(cls, socket, payload):
        outgoing_payload_length = len(payload) + 3  # Accounts for b'' characters that will also be amended.
        socket.send(encode_and_apply_padding(outgoing_payload_length, PADDED_MESSAGE_SIZE))
        # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
        confirmation = cls._receive_confirmation(socket)
        if confirmation:
            socket.send(payload.encode())
        else:
            # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
            pass

    @staticmethod
    def receive_data(socket):
        incoming_payload_length = decode_and_remove_padding(socket.recv(PADDED_MESSAGE_SIZE))
        print(f'Client received size of next message: "{incoming_payload_length}"')
        socket.send(CONFIRMATION_CODE.encode())
        payload = socket.recv(incoming_payload_length).decode()
        return payload

    @classmethod
    def _receive_confirmation(cls, socket):
        confirmation = socket.recv(len(CONFIRMATION_CODE))
        return True if confirmation == CONFIRMATION_CODE.encode() else False
