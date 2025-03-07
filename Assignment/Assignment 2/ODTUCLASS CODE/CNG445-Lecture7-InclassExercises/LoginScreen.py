from tkinter import *
from tkinter import messagebox

class LoginScreen(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Login")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.userNameLabel = Label(self.frame1, text="Username")
        self.userNameLabel.pack(side=LEFT, padx=5, pady=5)

        self.userNameEntry = Entry(self.frame1, name="username")
        self.userNameEntry.pack(side=LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.passwordLabel = Label(self.frame2, text="Password")
        self.passwordLabel.pack(side=LEFT, padx=5, pady=5)

        self.passwordEntry = Entry(self.frame2, name="password", show="*")
        self.passwordEntry.pack(side=LEFT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.loginButton = Button(self.frame3, text="Login", command = self.ButtonPressed)
        self.loginButton.pack(side=LEFT, padx=5, pady=5)

    def ButtonPressed(self):
        username = self.userNameEntry.get()
        password = self.passwordEntry.get()
        #Write some code to check their validity
        messagebox.showinfo("Message", "Welcome " + username + "\nLogin Successful")

if __name__ == "__main__":
    window = LoginScreen()
    window.mainloop() #show the window





