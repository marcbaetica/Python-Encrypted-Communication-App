import os
import threading
from dotenv import load_dotenv
from lib.comms_protocol import CommsProtocolHandler
from communication_protocols.comms_protocol_factory import comms_protocol_factory


load_dotenv()

EXIT_CODE = os.getenv('EXIT_CODE')
COMMUNICATION_PROTOCOL_TYPE = 'Basic'  # Can also be 'Advanced'


class ChatHandler:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name
        self.comms_protocol = comms_protocol_factory(self.socket, COMMUNICATION_PROTOCOL_TYPE)

    def handle_chat(self):
        while True:
            incoming_messages = threading.Thread(target=self.handle_receive_messages, daemon=True)
            incoming_messages.start()
            self.handle_sending_messages()

    def handle_sending_messages(self):
        # Daemon thread. Should be killed when input terminates execution.
        data_to_send = ''
        while data_to_send == '':  # Empty payloads are synonymous to connection closing.
            data_to_send = input(f'[{self.name}] Data to send ({EXIT_CODE} to close connection): ')
        if not CommsProtocolHandler.is_close_socket_attempt(data_to_send, self.socket.getpeername(), self.name):
            CommsProtocolHandler.send_data_attempt(self.socket, data_to_send)
        else:
            self.socket.close()

    def handle_receive_messages(self):
        try:
            data_received = CommsProtocolHandler.receive_data_attempt(self.socket, self.name)
            if not CommsProtocolHandler.is_other_party_socket_closed(data_received, self.socket.getpeername(), self.name):
                print(f'[{self.name}] Received message: {data_received}')
            else:
                self.socket.close()
        except OSError as e:
            # When socket has been terminated, all subsequent operations involving the object should simply break.
            # Specific scenario logging has been accounted for.
            # OSError: [WinError 10038] An operation was attempted on something that is not a socket
            pass  # TODO: move this to break loop
