from tkinter import *
from tkinter import messagebox
from storePanel import StorePanel
from analystPanel import AnalystPanel

class LoginScreen(Frame):
    def __init__(self, clientSocket):
        Frame.__init__(self)
        self.clientSocket = clientSocket
        self.master.title("Login")
        self.pack(padx=10, pady=10)

        # username filed
        self.userNameLabel = Label(self, text="Username:")
        self.userNameLabel.grid(row=0, column=0, sticky=W, pady=5)
        self.userNameEntry = Entry(self)
        self.userNameEntry.grid(row=0, column=1, pady=5)

        # password field to get the password from the user and process it later
        self.passwordLabel = Label(self, text="Password:")
        self.passwordLabel.grid(row=1, column=0, sticky=W, pady=5)
        self.passwordEntry = Entry(self, show="*")
        self.passwordEntry.grid(row=1, column=1, pady=5)

        # login button to submit the details
        self.loginButton = Button(self, text="Login", command=self.handleLogin)
        self.loginButton.grid(row=2, column=0, columnspan=2, pady=10)


    #handlelogin will be resposible for sending the details to the server to check the info with user.txt and it will redirect the user to the correct pannel according to the role.

    def handleLogin(self):
        userName = self.userNameEntry.get()
        password = self.passwordEntry.get()
        #to make sure that both fields are filled
        if not userName or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            # send login details to the server
            loginMessage = f"login;{userName};{password}"
            self.clientSocket.send(loginMessage.encode())

            # receive response from the server
            serverResponse = self.clientSocket.recv(1024).decode()
            if serverResponse.startswith("loginsuccess"):
                _, _, role = serverResponse.split(";")
                messagebox.showinfo("Success", f"Welcome {userName} ({role})!")
                self.master.destroy()  # Close the login screen
                self.redirectToPanel(role,userName)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        #this exception because i was getting some kind of errors, I did it to debug them.
        except Exception as error:
            messagebox.showerror("Error", f"An unexpected error occurred: {error}")


    #this method will redirect the user to the related panel

    def redirectToPanel(self, role,userName):
        # redirect to the appropriate panel
        if role == "store":
            StorePanel(self.clientSocket,userName).mainloop()
        elif role == "analyst":
            AnalystPanel(self.clientSocket).mainloop()
