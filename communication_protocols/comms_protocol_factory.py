from communication_protocols.comms_protocol_basic_handler import BasicCommsProtocolHandler
from communication_protocols.comms_protocol_advanced_handler import AdvancedCommsProtocolHandler


def comms_protocol_factory(socket, type):
    """Factory for creating the type of communications protocol to apply.

    :param socket: (Socket) Socket object that the protocol will use.
    :param type: (String) Type of protocol to use in the chat. Currently supporting 'basic' and 'advanced).
    :return: Communications protocol object.
    """

    supported_types = ['basic', 'advanced']
    if type == 'basic':
        return BasicCommsProtocolHandler(socket)
    if type == 'advanced':
        return AdvancedCommsProtocolHandler(socket)
    else:
        raise ValueError(f'{type} is not a supported communications protocol type. Only {supported_types} are supported.')