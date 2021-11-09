import os
from dotenv import load_dotenv
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


load_dotenv()

PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
ACK_CODE = os.getenv('ACK_CODE')
EXIT_CODE = os.getenv('EXIT_CODE')


class CommsProtocolHandler:

    @classmethod
    def send_data(cls, socket, payload):
        outgoing_payload_length = len(payload) + 3  # Accounts for b'' characters that will also be amended.
        try:
            socket.send(encode_and_apply_padding(outgoing_payload_length, PADDED_MESSAGE_SIZE))
        except ConnectionResetError:
            print('[ERROR] Connection was unexpectedly severed by other party. Closing this connection as well.')
            socket.close()
        # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
        confirmation = cls._receive_confirmation(socket)
        if confirmation:
            socket.send(payload.encode())
        else:
            # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.
            pass

    @staticmethod
    def receive_data(socket, who):
        if who not in ['Server', 'Client']:
            raise ValueError(f'Parameter destination can only have values "Server" or "Client". Value received: {who}')
        try:
            header = socket.recv(PADDED_MESSAGE_SIZE)
            # TODO: revisit this scenario. Empty string while blocking might mean something else.
            if header == b'':  # Client socket closed due to no incoming data.
                return header
        except ConnectionResetError as e:
            print('[ERROR] Connection was unexpectedly severed by other party. Closing this connection as well.')
            socket.close()
            return  # TODO: handle this scenario as well in both client and server sockets.
        incoming_payload_length = decode_and_remove_padding(header)
        print(f'{who} received size of next message: "{incoming_payload_length}"')
        print(ACK_CODE)
        socket.send(ACK_CODE.encode())
        payload = socket.recv(incoming_payload_length).decode()
        return payload

    @classmethod
    def _receive_confirmation(cls, socket):
        confirmation = socket.recv(len(ACK_CODE))
        return True if confirmation == ACK_CODE.encode() else False

    @staticmethod
    def is_close_socket_attempt(message, address):
        if message == EXIT_CODE:
            print(f'[Client] Closing connection to {address[0]}:{address[1]}.')
            return True

    @staticmethod
    def is_other_party_socket_closed(message, address):
        if message == b'':
            print(f'[Client] The server has closed the connection on {address[0]}:{address[1]}.'
                  f' Closing socket from our end as well.')
            return True
        return False
