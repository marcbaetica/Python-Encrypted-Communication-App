from socket_libs.client_socket import ClientSocket


c = ClientSocket()
c.connect()

data_to_send = 'The bird is out of the nest!'

# TODO: Message size should be handled automatically in ClientSocket class.
c.send_data(len(data_to_send))
confirmation = c.receive_data()  # TODO: Handle error cases... dropped signal, collisions, reconfirm, etc.

c.send_data(data_to_send)  # Revisit to not need to encode here.
c.receive_data()
