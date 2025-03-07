from socket import *
from threading import *
class ClientThread(Thread):

    def __init__(self,clientsocket,clientaddress):
        Thread.__init__(self)
        self.clientsocket=clientsocket
        self.clientaddress=clientaddress
        print(f"Connection successful from {self.clientaddress}")

    def run(self):
        servermsg= "SERVER>>CONNECTION SUCCESSFUL".encode()#we always encode when we send
        self.clientsocket.send(servermsg)
        clientmsg= self.clientsocket.recv(1024).decode()# we always decode when we recieve to understand the message

        while clientmsg != "CLIENT>>BYE":
            servermsg= clientmsg.replace("CLIENT>>","SERVER>>").encode()
            self.clientsocket.send(servermsg)
            clientmsg= self.clientsocket.recv(1024).decode()
        print("Connection is disconnected from ", self.clientaddress)
        self.clientsocket.close()


if __name__== "__main__":
    HOST="127.0.0.1"
    PORT = 5000


    serversocket= socket(AF_INET, SOCK_STREAM)#(HOST,PORT) FAMILY AND TCP MODULE
    serversocket.bind((HOST,PORT))#FOR BINDING THE server
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)#update the options for the socket=> resuable

    while True:
        serversocket.listen()
        clientsocket, clientaddress = serversocket.accept()
        newClient = ClientThread(clientsocket,clientaddress)
        newClient.start()
