from socket import *
from threading import *
class ClientThread(Thread):

    def __init__(self, clientsocket, clientaddress):
        Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientaddress = clientaddress
        print("Connection successful from ", self.clientaddress)

    def run(self):
        servermsg = "SERVER>>CONNECTION SUCCESSFUL".encode()
        self.clientsocket.send(servermsg)
        clientmsg = self.clientsocket.recv(1024).decode()
        while clientmsg != "CLIENT>>BYE":
            servermsg = clientmsg.replace("CLIENT>>","SERVER>>").encode()
            self.clientsocket.send(servermsg)
            clientmsg = self.clientsocket.recv(1024).decode()
        print("Connection is disconneted from ", self.clientaddress)
        self.clientsocket.close()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000

    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    while True:
        serversocket.listen()
        clientsocket, clientaddress = serversocket.accept()
        newClient = ClientThread(clientsocket, clientaddress)
        newClient.start()