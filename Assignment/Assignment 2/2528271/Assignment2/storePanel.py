from tkinter import *
from tkinter import messagebox

class StorePanel(Frame):
    def __init__(self, clientSocket,storename):
        Frame.__init__(self) #super.__init__(self)
        self.storename=storename
        self.clientSocket = clientSocket
        self.master.title("Store Panel")
        self.pack(padx=20, pady=20)

        # Header Label
        self.headerLabel = Label(self, text="Items", font=("Arial", 14, "bold"))
        self.headerLabel.grid(row=0, column=0, columnspan=4, pady=10)

        # Item List
        self.items = [
            "Basic T-shirt",
            "Leather Jacket",
            "Robe of the Weave",
            "Plaid Shirt",
            "D4C Graphic T-shirt",
            "Denim Jeans",
            "Hodd-Toward Designer Shorts",
        ]

        self.quantityVars = []
        self.colorVars = []
        self.itemVars = []
        #enumerate is used to keep track of the index and the value itself, and it will loop through all the items since we will have the same structure
        for i, item in enumerate(self.items):
            # Checkbox for item selection
            itemVar = IntVar()
            itemCheck = Checkbutton(self, text=item, variable=itemVar)
            itemCheck.grid(row=i + 1, column=0, sticky=W+S)
            self.itemVars.append(itemVar)

            # quantity entry
            quantityLabel = Label(self, text="Quantity:")
            quantityLabel.grid(row=i + 1, column=1, padx=5)
            quantityVar = StringVar()
            quantityEntry = Entry(self, textvariable=quantityVar, width=5)
            quantityEntry.grid(row=i + 1, column=2)
            self.quantityVars.append(quantityVar)

            color = Label(self, text="Color:")
            color.grid(row=i + 1, column=3, padx=5)

            # color radio buttons, we can see that they are grouped through colorvar
            colorVar = StringVar(value="Red")
            redRadio = Radiobutton(self, text="Red", variable=colorVar, value="Red")
            redRadio.grid(row=i + 1, column=4, sticky=W)
            blackRadio = Radiobutton(self, text="Black", variable=colorVar, value="Black")
            blackRadio.grid(row=i + 1, column=5, sticky=W)
            self.colorVars.append(colorVar)

        # customer name input
        self.customerNameLabel = Label(self, text="Customer name:")
        self.customerNameLabel.grid(row=len(self.items) + 1, column=0, pady=10, sticky=W)
        self.customerNameEntry = Entry(self, width=20)
        self.customerNameEntry.grid(row=len(self.items) + 1, column=1, columnspan=3, pady=10)

        # Buttons for different purposes
        self.purchaseButton = Button(self, text="Purchase", command=self.handlePurchase)
        self.purchaseButton.grid(row=len(self.items) + 2, column=1, pady=10)
        self.returnButton = Button(self, text="Return", command=self.handleReturn)
        self.returnButton.grid(row=len(self.items) + 2, column=2, pady=10)
        self.closeButton = Button(self, text="Close", command=self.closeConnection)
        self.closeButton.grid(row=len(self.items) + 2, column=3, pady=10)

    #this method will close the server-client connection when close button is clicked
    def closeConnection(self):
        try:
            # notify the server about disconnection which will be handeled in the server side
            self.clientSocket.send("disconnect".encode())
            self.clientSocket.close()  # close the socket connection
        except Exception as e:
            print(f"Error while closing connection: {e}")
        finally:
            self.master.destroy()  # destroy the  window

    def handlePurchase(self):
        self.handleOperation("purchase")

    def handleReturn(self):
        self.handleOperation("return")

    def handleOperation(self, operationType):
        selectedItems = []
        totalQuantity = 0

        # collect selected items, quantities, and colors
        for i, itemVar in enumerate(self.itemVars):
            if itemVar.get():  # Check if the item is selected
                quantity = self.quantityVars[i].get()
                color = self.colorVars[i].get()
                #to handle weird situations
                if not quantity.isdigit() or int(quantity) <= 0:
                    messagebox.showerror("Error", f"Invalid quantity for {self.items[i]}")
                    return
                selectedItems.append(f"{quantity}-{i + 1}-{color}")
                totalQuantity += int(quantity)

        # Ensure at least one item is selected
        if not selectedItems:
            messagebox.showerror("Error", "Please select at least one item.")
            return

        # Ensure customer name is provided
        customerName = self.customerNameEntry.get().strip()
        if not customerName:
            messagebox.showerror("Error", "Customer name is required.")
            return

        # Create operation message in the required format
        operationMessage = f"{operationType};{self.storename};{totalQuantity};{','.join(selectedItems)};{customerName}"
        print(f"Sending message to server: {operationMessage}")  # debugging, i have issue here

        try:
            # Send operation message to the server
            self.clientSocket.send(operationMessage.encode())
            # Receive and process server response
            serverResponse = self.clientSocket.recv(1024).decode()
            print(f"Server response: {serverResponse}")  # debugging
            if serverResponse.startswith(f"{operationType}success"):
                totalCost = serverResponse.split(";")[1]
                messagebox.showinfo("Success",
                                    f"{operationType.capitalize()} operation completed successfully! Total Cost: {totalCost}")
            elif serverResponse.startswith("availabilityerror"):
                errorDetails = serverResponse.split(";")[1]
                messagebox.showerror("Error", f"Unavailable items: {errorDetails}")
            else:
                messagebox.showerror("Error", serverResponse)
        except Exception as e:
            print(f"Error communicating with the server: {e}")
            messagebox.showerror("Error", "Failed to communicate with the server.")


