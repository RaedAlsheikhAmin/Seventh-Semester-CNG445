from socket import *
from threading import *
from math import *

class ClientThread(Thread):
    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress

    def run(self):
        # wordlist=[]
        # meaninglist=[]
        dictionary={}
        with open("dictionary.txt","r") as df:
            for line in df:
                parts=line.strip().split(";")
                word=parts[0]
                meaning=parts[1]
                # wordlist.append(word)
                # meaninglist.append(meaning)
                dictionary[word]=meaning
        msg = "Welcome".encode()
        self.clientsocket.send(msg)
        while True:
            # index=0
            data = self.clientsocket.recv(1024).decode()
            if data == "bye":
                 break
            # if data in wordlist:
            #     for w in wordlist:
            #         if w==data:
            #             break;
            #         index = index + 1
            # result=meaninglist[index]

            result=dictionary[data]
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