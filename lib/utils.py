def print_container_details(container):
    """Takes a container of interest and prints details pertaining to that container: length, type and actual container.
    Used for debugging purposes.

    :param container: A sequnece data structure: string, bytes, etc.
    :return: None
    """
    print(len(container), type(container), container)


def encode_and_apply_padding(payload_size_bytes, total_length):  # TODO: Make total_length an env variable.
    """Takes the number of bytes the message will require and applies left-ASCII-0-padding if needed. Throws
    OverflowException if total size occupies more than the proposed lenght. Communication protocol requires the
    size of the upcoming message to be broadcasted before message gets sent. Hence the padding is capped to allow
    the socked to avoid extracting characters from the message.

    :param payload_size_bytes: (int) The length of the followup message that will be sent.
    :param total_length: (int) The length of the total padded message that will be sent.
    :return: (bytes) The padded message.
    """
    payload_size_bytes = str(payload_size_bytes).encode()
    if len(str(len(payload_size_bytes))) > total_length:  # TODO: Better way to calculate length of the char size.
        raise OverflowError(f'The string you are trying to send is larger than the allowed {10^total_length} bytes.')
    payload_size_bytes = payload_size_bytes.zfill(total_length)
    return payload_size_bytes


def decode_and_remove_padding(padded_payload_size_bytes):
    """Method reverses the effects of apply_padding(...). See its description for more details.

    :param padded_payload_size_bytes: (string) The padded message.
    :return: (int) The length of the followup message that will be sent.
    """
    return int(padded_payload_size_bytes)


# TODO: remove this later
# For testing purpose
if __name__ == '__main__':
    total_bytes_count = 2134534
    total_bytes_needed = 10  # 1GB max

    padded_message = encode_and_apply_padding(total_bytes_count, total_bytes_needed)
    print_container_details(padded_message)

    message = decode_and_remove_padding(padded_message)
    print(message, type(message))
