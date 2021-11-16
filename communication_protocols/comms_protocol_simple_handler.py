from communication_protocols.comms_protocol_basic import SimpleCommsProtocolHandler


class BasicCommsProtocolHandler:
    def __init__(self, socket):
        self.socket = socket
