from communication_protocols.comms_protocol_basic import BasicCommsProtocol


class BasicCommsProtocolHandler:
    def __init__(self, socket):
        self.socket = socket
