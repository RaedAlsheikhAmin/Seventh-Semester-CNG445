from socket import *
from tkinter import *
from tkinter import messagebox

class ClientScreen(Frame):
    def __init__(self,clientsocket):
        Frame.__init__(self)
        self.clientsocket= clientsocket

        servermsg= self.clientsocket.recv(1024).decode()
        print(servermsg)

        self.master.title("Fahrenheit -> Celsius")
        self.pack() #to use the pack manager
        self.msgLabel= Label(self, text="Fahrenheit:")
        self.msgLabel.pack(padx=5, pady=5)
        self.msgEntry= Entry(self)
        self.msgEntry.pack(padx=5, pady=5)
        self.sendButton = Button(self, text="Conver it to Celsius",command=self.sendMessage)
        self.sendButton.pack(padx=5, pady=5)

    def sendMessage(self):
        clientmsg= (self.msgEntry.get())
        clientmsg = (5 / 9) * (float(clientmsg) - 32)
        self.clientsocket.send(str(clientmsg).encode())

        if(self.msgEntry.get()== "BYE"):
            self.clientsocket.close()
            self.master.destroy()#to close the GUI
        else:
            servermsg = self.clientsocket.recv(1024).decode()
            messagebox.showinfo("Celsius Equivalent",f"{self.msgEntry.get()} Fahrenheit = {(servermsg) } Celsius" )






if __name__== "__main__":
    HOST= "127.0.0.1"
    PORT= 5000
    clientsocket= socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((HOST,PORT))
    window = ClientScreen(clientsocket)
    window.mainloop()#to show the GUI on the screen