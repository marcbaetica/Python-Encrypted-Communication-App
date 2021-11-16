"""Basic communication protocol. Does not support a retry transmission handling mechanism. Assumes messages are no
longer than 1024 bytes."""

from communication_protocols.comms_protocol_base_class import BaseCommsProtocolHandler


class SimpleCommsProtocolHandler(BaseCommsProtocolHandler):
    def __init__(self, socket):
        self.socket = socket

    def receive_message_attempt(self):
        return self.socket.recv(1024).decode()

    def send_message_attempt(self, message):
        self.socket.send(message.encode())
