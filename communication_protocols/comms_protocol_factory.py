from communication_protocols.comms_protocol_basic import BasicCommsProtocol
from communication_protocols.comms_protocol_advanced import AdvancedCommsProtocol


def comms_protocol_factory(socket, type):
    """Factory for creating the type of communications protocol to apply.

    :param socket: (Socket) Socket object that the protocol will use.
    :param type: (String) Type of protocol to use in the chat. Currently supporting 'basic' and 'advanced).
    :return: Communications protocol object.
    """

    supported_types = ['basic', 'advanced']
    if type == 'basic':
        return BasicCommsProtocol(socket)
    if type == 'advanced':
        return AdvancedCommsProtocol(socket)
    else:
        raise ValueError(f'{type} is not a supported communications protocol type. Only {supported_types} are supported.')