import socket


client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_s.bind(('localhost', 55000))
server_s.listen(1)
client_s.connect(('localhost', 55000))
new_client_s, addr = server_s.accept()



print(client_s, server_s, new_client_s, addr)

# have P2P conversation:
# client_s.send(...)
# new_client_s.recv(...)