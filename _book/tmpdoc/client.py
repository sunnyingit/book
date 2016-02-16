import socket

HOST, PORT = 'localhost', 8888

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fd = socket.connect((HOST, PORT))
message = "hello world"
socket.send(message)
while True:
    data = socket.recv(5)
    print data
socket.close()
