from socket import *
from loginScreen import LoginScreen

class ClientApplication:
    def __init__(self, host, port):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((host, port))
        self.loginScreen = LoginScreen(self.clientSocket)

    def run(self):
        self.loginScreen.mainloop()

if __name__ == "__main__":
    client= ClientApplication("127.0.0.1", 5000)
    client.run()
