from communication_protocols.comms_protocol_simple_handler import SimpleCommsProtocolHandler
from communication_protocols.comms_protocol_advanced_handler import AdvancedCommsProtocolHandler


def comms_protocol_factory(socket, type):
    """Factory for creating the type of communications protocol to apply.

    :param socket: (Socket) Socket object that the protocol will use.
    :param type: (String) Type of protocol to use in the chat. Currently supporting 'simple' and 'advanced).
    :return: Communications protocol object.
    """

    supported_types = ['basic', 'advanced']
    if type == 'simple':
        return SimpleCommsProtocolHandler(socket)
    if type == 'advanced':
        return AdvancedCommsProtocolHandler(socket)
    else:
        raise ValueError(f'{type} is not a supported communications protocol type. Only {supported_types} are supported.')