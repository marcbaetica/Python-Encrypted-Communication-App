from socket_libs.client_socket import ClientSocket


c = ClientSocket('localhost')

# For testing purposes
# data_to_send = 'The bird has left the nest!'
# c.send_data_attempt(data_to_send)


# TODO: should connections be closed from handler closing connection or simply dropped?
while True:
    data_to_send = input('[Client] Data to send ("bye" to exit): ')
    c.send_data_attempt(data_to_send)  # Send even 'bye' to notify client of connection close
    reply = c.receive_data_attempt()
    if data_to_send == 'bye':
        c.close()
        break

# TODO: wait for server to confirm that they understood that the connection is over.
# Question: is this even needed?

