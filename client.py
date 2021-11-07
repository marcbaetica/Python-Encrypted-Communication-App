from socket_libs.client_socket import ClientSocket


c = ClientSocket('localhost')

data_to_send = 'The bird has left the nest!'

c.send_data_attempt(data_to_send)  # Revisit to not need to encode here.
reply = c.receive_data(1024)
