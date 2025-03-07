from socket import *
from tkinter import *
from tkinter import messagebox

class ClientApplication(Frame):
    def __init__(self, host, port):
        Frame.__init__(self)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((host, port))

        self.master.title("Semester details")
        self.pack(padx=10, pady=10)

        self.Year = Label(self, text="Year ")
        self.Year.grid(row=0, column=0, sticky=W+S, pady=5)
        self.YearEntry = Entry(self)
        self.YearEntry.grid(row=0, column=1, pady=5)

        self.semestervar = StringVar(value="Fall Semester") #for the default one
        self.firstRadio = Radiobutton(self, text="Fall Semester", variable=self.semestervar, value="1")
        self.firstRadio.grid(row=1, column=0, sticky=W+S)
        self.secondRadio = Radiobutton(self, text="Spring Semester", variable=self.semestervar, value="2")
        self.secondRadio.grid(row=1, column=1, sticky=W+S)

        self.itemVar = IntVar()
        self.itemCheck = Checkbutton(self, text="Only multiple Sections", variable=self.itemVar)
        self.itemCheck.grid(row=2, column=0, sticky=W + S)

        self.Getcourses = Button(self, text="Get Courses", command=self.handleCourses)
        self.Getcourses.grid(row=3, column=0, pady=10)
        self.Clear = Button(self, text="Clear", command=self.handleClear)
        self.Clear.grid(row=3, column=1, pady=10)
        self.Close = Button(self, text="Close", command=self.handleClose)
        self.Close.grid(row=3, column=2, pady=10)

    def run(self):
        pass


    def handleClear(self):
        self.semestervar = StringVar(value="Fall Semester")  # for the default one
        self.itemVar = 0

    def handleClose(self):
            try:
                # notify the server about disconnection which will be handeled in the server side
                self.clientSocket.send("disconnect".encode())
                self.clientSocket.close()  # close the socket connection
            except Exception as e:
                print(f"Error while closing connection: {e}")
            finally:
                self.master.destroy()  # destroy the  window

    def handleCourses(self):
        yearentered= self.YearEntry.get()
        if(yearentered ==""):
            messagebox.showerror("Error year","Missing year")
            return
        if(int(yearentered) < 1990):
            messagebox.showerror("Year restriction","Invalid Year")
            return

        checkbox = self.itemVar.get()  # Check if the item is selected
        radiobutton= self.semestervar.get() #this will reutnr fall semester or sprint semester
        clientmessage= f"GetCourse;{yearentered};{radiobutton};{checkbox}"
        self.clientSocket.send(clientmessage.encode())


        serverresponse=  self.clientSocket.recv(1024).decode()
        if "nocourse" in serverresponse:
            messagebox.showinfo("No course","No courses has been found")
        else:# i should show the courses here , we need to use split(;) that we get the courses and the sections, and display it to the user
            pass




if __name__ == "__main__":
    client = ClientApplication("127.0.0.1", 5000)
    client.run()
    client.mainloop()