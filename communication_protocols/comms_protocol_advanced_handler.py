from time import sleep
from communication_protocols.comms_protocol_advanced import AdvancedCommsProtocol


class AdvancedCommsProtocolHandler:
    def __init__(self, socket):
        self.socket = socket
        self.comms_protocol = AdvancedCommsProtocol(socket)

    def send_message_attempt(self, message):
        self.comms_protocol.send_incoming_payload_size(message)
        if not self.comms_protocol.is_message_size_confirmation_received():
            # if no confirmation, re-send length, repeat 10 times. If still no result, raise conn failed + close socket
            pass  # TODO: what if it doesn't arrive on time?
        self.comms_protocol.send_message(message)
        if not self.comms_protocol.is_message_size_confirmation_received():
            # if no confirmation, re-send message, repeat 10 times. If still no result, raise conn failed + close socket
            pass  # TODO: what if it doesn't arrive on time?

    def receive_message_attempt(self):
        try:
            incoming_message_size = self.comms_protocol.receive_incoming_payload_size()
            self.comms_protocol.send_message_size_confirmation()
            message = self.comms_protocol.receive_message(incoming_message_size)
            self.comms_protocol.send_message_confirmation()
            return message
        except ConnectionError as e:
            # Python socket behavior is expected to hang upon attempting to read from the network buffer.
            # If other party socket is closed, the network buffer receive method call returns empty byte array.
            # Hence, socket needs to be closed.
            self.socket.close()
            print(f'Connection error: {e}')
            return
        except OSError as e:
            # When socket has been terminated, all subsequent operations involving the object should simply break.
            # Specific scenario logging has been accounted for.
            # OSError: [WinError 10038] An operation was attempted on something that is not a socket
            self.socket.close()
