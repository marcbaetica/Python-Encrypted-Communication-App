import os
import threading
from dotenv import load_dotenv
from communication_protocols.comms_protocol_factory import comms_protocol_factory


load_dotenv()

EXIT_CODE = os.getenv('EXIT_CODE')
COMMUNICATION_PROTOCOL_TYPE = 'simple'  # Supports 'simple' or 'advanced'.


class ChatHandler:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name
        self.comms_protocol = comms_protocol_factory(self.socket, COMMUNICATION_PROTOCOL_TYPE)

    def handle_chat(self):
        incoming_messages = threading.Thread(target=self.handle_receive_messages, daemon=True)
        incoming_messages.start()
        while True:
            self.handle_sending_messages()

    def handle_sending_messages(self):
        # Daemon thread. Should be killed when input terminates execution.
        message = None
        while message != EXIT_CODE:
            message = input(f'[{self.name}] Message to send ({EXIT_CODE} to close connection): ')
            self.comms_protocol.send_message_attempt(message)
        print(f'Received exit code [{EXIT_CODE}]. Closing socket.')
        self.socket.close()  # Empty payloads are synonymous to connection closing.

    def handle_receive_messages(self):
        while True:
            data_received = self.comms_protocol.receive_message_attempt()
            # TODO: closing side results in:
            #  ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host.
            print(f'[{self.name}] Received message: {data_received}')
