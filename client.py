from socket_libs.client_socket import ClientSocket


c = ClientSocket()

c.connect()
c.send_data(b'The bird is out of the nest!')
c.receive_data()
