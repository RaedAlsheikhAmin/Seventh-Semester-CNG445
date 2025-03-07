from socket import *
from threading import *
from math import *

class ClientThread(Thread):
    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress

    def run(self):
        msg = "Welcome".encode()
        self.clientsocket.send(msg)
        while True:
            data = self.clientsocket.recv(1024).decode()
            if data == "bye":
                break
            result = eval(data)
            self.clientsocket.send(str(result).encode())
        self.clientsocket.close()

HOST = "127.0.0.1"
PORT = 5000

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print("Server is starting")
print("Waiting for connection requests")

while True:
    server.listen()
    clientsocket, clientaddress = server.accept()
    newThread = ClientThread(clientsocket, clientaddress)
    newThread.start()