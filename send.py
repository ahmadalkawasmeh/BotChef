#client (send)

import socket
import IPService

TCP_IP = IPService.get_ip("Pi3")
TCP_PORT = IPService.get_port("Pi3")
BUFFER_SIZE = 1024
MESSAGE = "3/2"
print(IPService.get_local_ip_address())
IPService.save_ip(IPService.get_local_ip_address())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
data = s.recv(BUFFER_SIZE)
s.close()

print("Received data: ", data.decode())
