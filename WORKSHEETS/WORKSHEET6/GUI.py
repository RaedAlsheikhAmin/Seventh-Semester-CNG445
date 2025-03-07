from tkinter import *
from tkinter import messagebox
#NAMES OF THIS PACKAGE SHOULD BE LOWERCASE
#NAMES SHOULD BE UNIQUE FOR PARTICULAR MEMBER, IF USED MULTIPLE TIMES, THE LAST ONE WILL BE APPLIED
#
class LoginScreen(Frame):
    def __init__(self):#ALWAYS PACK THEM THAT YOU GET THEM IN THE LAYOUT
        Frame.__init__(self)
        self.pack()#pack manager
        self.master.title("Login")


        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.userNameLabel = Label(self.frame1,name="username", text="Username")
        self.userNameLabel.pack(side=LEFT,padx=5, pady=5)

        self.userNameEntry = Entry(self.frame1, name="something")
        self.userNameEntry.pack(side=LEFT ,padx=5, pady=5)

        self.frame2= Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.passwordLabel = Label(self.frame2, text="password")
        self.passwordLabel.pack(side=LEFT, padx=5, pady=5)


        self.passwordEntry = Entry(self.frame2, name="password", show="*")#the show part is the stars that we see when we enter password
        self.passwordEntry.pack(side=LEFT, padx=5, pady=5)

        self.frame3= Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.loginButton= Button(self.frame3, text="Login", command = self.ButtonPressed)#ACTION FOR THE BUTTON
        self.loginButton.pack(side=LEFT, padx=5, pady=5)


    def ButtonPressed(self):
            username= self.userNameEntry.get()#to get the username from the txt box
            password= self.passwordEntry.get()

            #we can check for login validation here
            messagebox.showinfo("Message", f"Welcome {username}\n""Login Successful")

if __name__== "__main__":
    window = LoginScreen()
    window.mainloop()#show the window
