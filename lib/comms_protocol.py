# TODO: Document all methods in here.


import os
from dotenv import load_dotenv
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


load_dotenv()

PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
ACK_SIZE_CODE = os.getenv('ACK_SIZE_CODE')
ACK_MESSAGE_CODE = os.getenv('ACK_MESSAGE_CODE')
EXIT_CODE = os.getenv('EXIT_CODE')


class CommsProtocolHandler:

    @classmethod
    def send_data_attempt(cls, socket, payload):  # TODO: handle retries here.
        outgoing_payload_length = len(payload) + 3  # Accounts for b'' characters that will also be amended.
        try:
            socket.send(encode_and_apply_padding(outgoing_payload_length, PADDED_MESSAGE_SIZE))
        except ConnectionResetError:
            print('[ERROR] Connection was unexpectedly severed by other party. Closing this connection as well.')
            socket.close()
        # TODO: Handle error cases... collisions, reconfirm, etc.
        confirmation = cls._receive_confirmation(socket)
        if confirmation:
            socket.send(payload.encode())
        else:
            # TODO: Handle error cases... collisions, reconfirm, etc.
            pass

    @staticmethod
    def receive_data_attempt(socket, who):  # TODO: handle retries here.
        """Can receive:
         - nothing / blocked call -> idling means socket is still open and pending network buffer fill-in
         - instant empty bytes object (encoded message string) on all calls  -> other party socket has been closed
         - incoming message size (padded) -> message is about to be sent, pending confirmation
         - message size confirmation -> confirms that message has been received, therefore waiting for the message
         - actual message
         - confirmation of message received -> without this the other party will retry to sent the message

        :param socket: (Socket) Socket object to listen to.
        :param who: (String) Entity listening to this call. Used for logging. Can be either 'Server' or 'Client'.
        :return:
        """
        if who not in ['Server', 'Client']:
            raise ValueError(f'Parameter destination can only have values "Server" or "Client". Value received: {who}')
        try:
            potential_messages = [ACK_MESSAGE_CODE, ACK_SIZE_CODE, ACK_MESSAGE_CODE, EXIT_CODE]
            potential_message_sizes = [len(message) for message in potential_messages]
            max_message_size = max(potential_message_sizes)
            print(max_message_size)
            payload = socket.recv(max_message_size)
            if payload == b'':  # Client socket closed due to no incoming data.
                return payload
        except ConnectionResetError:
            print('[ERROR] Connection was unexpectedly severed by other party. Closing this connection as well.')
            socket.close()
            return
        print(payload)
        if payload.decode() == ACK_MESSAGE_CODE:
            pass
        else:
            incoming_payload_length = decode_and_remove_padding(payload)
            print(f'{who} received size of next message: "{incoming_payload_length}"')
            print(ACK_MESSAGE_CODE)  # TODO: handle this!
            socket.send(ACK_MESSAGE_CODE.encode())
            payload = socket.recv(incoming_payload_length).decode()
            return payload

    @classmethod
    def _receive_confirmation(cls, socket):
        confirmation = socket.recv(len(ACK_MESSAGE_CODE))
        return True if confirmation == ACK_MESSAGE_CODE.encode() else False

    @staticmethod
    def is_close_socket_attempt(message, address, who):
        if message == EXIT_CODE:
            print(f'[{who}] Closing connection to {address[0]}:{address[1]}.')
            return True

    @staticmethod
    def is_other_party_socket_closed(message, address, who):
        if message == b'':
            print(f'[{who}] The other party has closed the connection on {address[0]}:{address[1]}.'
                  f' Closing socket from our end as well.')
            return True
        return False
