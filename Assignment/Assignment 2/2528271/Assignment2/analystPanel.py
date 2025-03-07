from tkinter import *
from tkinter import messagebox

class AnalystPanel(Frame):
    def __init__(self, clientSocket):
        Frame.__init__(self)
        self.clientSocket = clientSocket
        self.master.title("Analyst Panel")
        self.pack(padx=10, pady=10)

        # Report Selection Label
        self.reportLabel = Label(self, text="Select a Report:")
        self.reportLabel.grid(row=0, column=0, pady=5)

        # Report Options
        self.reportOptions = [
            ("Most Bought Item", "report1"),
            ("Store with Highest Operations", "report2"),
            ("Total Income by Store", "report3"),
            ("Most Returned Color for Basic T-shirt", "report4"),
        ]

        self.reportVar = StringVar(value="report1")  # default selection
        for idx, (label, value) in enumerate(self.reportOptions):
            reportRadio = Radiobutton(self, text=label, variable=self.reportVar, value=value)
            reportRadio.grid(row=idx + 1, column=0, sticky=W)

        # Submit Button
        self.submitButton = Button(self, text="Get Report", command=self.getReport)
        self.submitButton.grid(row=len(self.reportOptions) + 1, column=0, pady=10)
        self.closeButton = Button(self, text="Close", command=self.closeConnection)
        self.closeButton.grid(row= len(self.reportOptions) + 1, column=1, pady=10)

    def closeConnection(self):
        try:
            # Notify the server about disconnection
            self.clientSocket.send("disconnect".encode())
            self.clientSocket.close()  # Close the socket connection
        except Exception as e:
            print(f"Error while closing connection: {e}")
        finally:
            self.master.destroy()  # Destroy the Tkinter window

    def getReport(self):
        selectedReport = self.reportVar.get()
        self.clientSocket.send(selectedReport.encode())
        #getting the server response
        serverResponse = self.clientSocket.recv(1024).decode()
        messagebox.showinfo("Report: ", f"Server Response:\n{serverResponse}")
