from time import sleep
from communication_protocols.comms_protocol_advanced import AdvancedCommsProtocol


class AdvancedCommsProtocolHandler:
    def __init__(self, socket):
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
