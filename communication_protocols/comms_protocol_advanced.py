"""Advanced communication protocol. Supports a retry transmission handling mechanism and a fixed incoming payload size
transmission."""

"""TODO: remove this!
Can receive / send:
 - nothing / blocked call -> idling means socket is still open and pending network buffer fill-in
 - instant empty bytes object (encoded message string) on all calls  -> other party socket has been closed
 - incoming message size (padded) -> message is about to be sent, pending confirmation
 - message size confirmation -> confirms that message has been received, therefore waiting for the message
 - actual message
 - confirmation of message received -> without this the other party will retry to sent the message
"""


import os
from dotenv import load_dotenv
from lib.utils import decode_and_remove_padding, encode_and_apply_padding


load_dotenv()

PADDED_MESSAGE_SIZE = int(os.getenv('PADDED_MESSAGE_SIZE'))
ACK_SIZE_CODE = os.getenv('ACK_SIZE_CODE')
ACK_MESSAGE_CODE = os.getenv('ACK_MESSAGE_CODE')


class AdvancedCommsProtocol:
    def __init__(self, socket):
        self.socket = socket

    def send_incoming_payload_size(self, message):
        self.socket.send(encode_and_apply_padding(len(message), PADDED_MESSAGE_SIZE))

    def receive_incoming_payload_size(self):
        return decode_and_remove_padding(self.socket.recv(PADDED_MESSAGE_SIZE))

    def send_message_size_confirmation(self):
        self.socket.send(ACK_SIZE_CODE.encode())

    def receive_message_size_confirmation(self):  # TODO: should be boolean?
        return self.socket.recv(len(ACK_SIZE_CODE)).decode()

    def send_message(self, message):
        self.socket.send(message.encode())

    def receive_message(self, message_length):
        return self.socket.recv(message_length).decode()

    def send_message_confirmation(self):
        self.socket.send(ACK_MESSAGE_CODE.encode())

    def receive_message_confirmation(self):  # TODO: should be boolean?
        return self.socket.recv(len(ACK_MESSAGE_CODE)).decode()

# TODO: handle exit codes?
