"""Basic communication protocol. Does not support a retry transmission handling mechanism. Assumes messages are no
longer than 1024 bytes."""


class BasicCommsProtocol:
    def __init__(self, socket):
        self.socket = socket

    def receive_message(self):
        return self.socket.recv(1024).decode()

    def send_message(self, message):
        self.socket.send(message.encode())
