import sys
from socket_libs.client_socket import ClientSocket


server_ip = sys.argv[1]
c = ClientSocket(server_ip)
