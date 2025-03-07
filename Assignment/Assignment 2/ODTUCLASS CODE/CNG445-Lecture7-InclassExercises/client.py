from socket import *
from tkinter import *
from tkinter import messagebox

class ClientScreen(Frame):
    def __init__(self, clientsocket):
        Frame.__init__(self)
        self.clientsocket = clientsocket
        servermsg = self.clientsocket.recv(1024).decode()
        print(servermsg)

        self.master.title("Client Screen")
        self.pack()

        self.msgLabel = Label(self, text="Message:")
        self.msgLabel.pack(padx=5, pady=5)

        self.msgEntry = Entry(self)
        self.msgEntry.pack(padx=5, pady=5)

        self.sendButton = Button(self, text="Send", command=self.sendMessage)
        self.sendButton.pack(padx=5, pady=5)

    def sendMessage(self):
        clientmsg = ("CLIENT>>" + self.msgEntry.get()).encode()
        self.clientsocket.send(clientmsg)
        if (self.msgEntry.get() == "BYE"):
            self.clientsocket.close()
            self.master.destroy()
        else:
            servermsg = self.clientsocket.recv(1024).decode()
            messagebox.showinfo("Message", servermsg)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5000
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    window = ClientScreen(clientsocket)
    window.mainloop()#to show on the screen