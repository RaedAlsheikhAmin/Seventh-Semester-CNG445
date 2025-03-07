from socket import *
from threading import *

# Lock for thread synchronization
fileLock = RLock()

# This is the constructor for the `ClientThread` class.
# It initializes the thread for each connected client and sets up their socket and address.
# Also, it prints a message confirming that a new client is connected.

class ClientThread(Thread):
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self) # super.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        print(f"Connection established with {clientAddress}")

    # This is the main function of the client thread that keeps running.
    # It listens for incoming messages from the client, processes commands (like login, purchase, return, or report requests),
    # and handles disconnections. Invalid commands are rejected with a message.
    # If something goes wrong, it closes the connection gracefully and logs an error
    def run(self):
        try:
            while True:
                # Receive and decode the client message and process it.
                clientMessage = self.clientSocket.recv(1024).decode()
                print(f"Received message: {clientMessage} from {self.clientAddress}")

                # Ignore empty messages
                if not clientMessage:
                    print(f"Empty message received from {self.clientAddress}. Ignoring.")
                    continue

                # Handle disconnection
                if clientMessage == "disconnect":
                    print(f"Client {self.clientAddress} has disconnected.")
                    break

                # handle login operation
                if clientMessage.startswith("login;"): # if "login" in clientMessage
                    self.handleLogin(clientMessage)

                #handling purchase or return operations
                elif clientMessage.startswith("purchase;") or clientMessage.startswith("return;"):
                    self.handleOperation(clientMessage)

                # handle report requests
                elif clientMessage.startswith("report"):
                    reportCode = clientMessage.strip()
                    self.processReport(reportCode)

                # Invalid command handling
                else:
                    print(f"Invalid command received: {clientMessage}")
                    self.clientSocket.send("Invalid command.".encode())

        except Exception as error:
            print(f"Error with client {self.clientAddress}: {error}")
        finally:
            self.clientSocket.close()
            print(f"Connection closed with {self.clientAddress}")

    # This function processes the login request from the client.
    # It checks the username and password against the `users.txt` file.
    # If a match is found, the role of the user is also sent back to the client with a success message.
    # Otherwise, it sends back a failure message.

    def handleLogin(self, message):
        _, userName, password = message.split(";") # _ will be the login itself
        with fileLock, open("users.txt", "r") as userFile:
            for line in userFile:
                storedUserName, storedPassword, role = line.strip().split(";")
                if userName == storedUserName and password == storedPassword:
                    successMessage = f"loginsuccess;{userName};{role}"
                    self.clientSocket.send(successMessage.encode())
                    return
        self.clientSocket.send("loginfailure".encode())


    # This function handles either a "purchase" or "return" operation.
    # It splits the incoming message into operation details and passes them to the appropriate function.
    # If the operation type is invalid or the message format is incorrect, it sends back an error message.

    def handleOperation(self, message):
        try:
            operationType, store, totalQuantity, items, customerName = message.split(";",4)
            itemsList = items.split(",")  # Parse item list

            if operationType == "purchase":
                self.processPurchase(store, int(totalQuantity), itemsList, customerName)
            elif operationType == "return":
                self.processReturn(store, int(totalQuantity), itemsList, customerName)
        except Exception as e:
            print(f"Error handling operation: {e}")
            self.clientSocket.send(f"{operationType}error;Invalid operation format.".encode())

    # This function processes report requests sent by the client.
    # Based on the report code, it generates the required statistics:
    # - report1: Finds the most bought item.
    # - report2: Finds the store with the highest number of operations.
    # - report3: Calculates total income by store.
    # - report4: Finds the most returned color for Basic T-shirts.
    # If the report code is invalid, it sends back an error message.

    def processReport(self, reportCode):
        try:
            with fileLock, open("operations.txt", "r") as operationsFile:
                operationsData = operationsFile.readlines()

            # Report 1: Most bought item(s)
            if reportCode == "report1":
                itemCounts = {}
                for line in operationsData:
                    if line.startswith("purchase"):
                        try:
                            _, _, _, items = line.strip().split(";", 3)
                            for item in items.split(";"):
                                quantity, itemID, color = item.split("-")
                                quantity = int(quantity)
                                itemCounts[(itemID, color)] = itemCounts.get((itemID, color), 0) + quantity
                        except ValueError:
                            print(f"value error purchase entry: {line.strip()}")

                if not itemCounts:
                    self.clientSocket.send("report1: No purchases yet.".encode())
                    return

                maxCount = max(itemCounts.values())
                mostBought = [f"{itemID}-{color}" for (itemID, color), count in itemCounts.items() if count == maxCount]
                self.clientSocket.send(f"report1: {','.join(mostBought)}".encode())

            # Report 2: Store with the highest operations
            elif reportCode == "report2":
                storeCounts = {}
                for line in operationsData:
                    if line.startswith("purchase") or line.startswith("return"):
                        try:
                            _, store, _, _ = line.strip().split(";", 3)
                            storeCounts[store] = storeCounts.get(store, 0) + 1
                        except ValueError:
                            print(f"Malformed operation entry: {line.strip()}")

                if not storeCounts:
                    self.clientSocket.send("report2;No operations yet.".encode())
                    return

                maxOps = max(storeCounts.values())
                topStores = [store for store, count in storeCounts.items() if count == maxOps]
                self.clientSocket.send(f"report2;{','.join(topStores)}".encode())

            # Report 3: Total income by store
            elif reportCode == "report3":
                storeIncome = {}
                for line in operationsData:
                    if line.startswith("purchase"):
                        try:
                            _, store, _, items = line.strip().split(";", 3)
                            for item in items.split(","):
                                quantity, itemID, color = item.split("-")
                                quantity = int(quantity)
                                price = self.getPrice(itemID, color)
                                storeIncome[store] = storeIncome.get(store, 0) + quantity * price
                        except ValueError:
                            print(f"Malformed purchase entry: {line.strip()}")

                if not storeIncome:
                    self.clientSocket.send("report3;No income yet.".encode())
                    return

                incomeReports = [f"{store}:{income}" for store, income in storeIncome.items()]
                self.clientSocket.send(f"report3;{','.join(incomeReports)}".encode())

            # Report 4: most returned color for Basic T-shirts
            elif reportCode == "report4":
                colorCounts = {}
                try:
                    # iterate over each operation line in operations.txt
                    for line in operationsData:
                        # process only "return" operations
                        if line.startswith("return"):
                            try:
                                _, _, _, items = line.strip().split(";", 3)  # extract returned items
                                # parse each item in the returned items list
                                for item in items.split(";"):
                                    quantity, itemID, color = item.strip().split("-")
                                    if itemID == "1":  # ID1 is basic t-shirt
                                        colorCounts[color] = colorCounts.get(color, 0) + int(quantity)
                            except ValueError:
                                print(f"wrong value return entry: {line.strip()}")

                    # Check if there are any returns for Basic T-shirts
                    if not colorCounts:
                        self.clientSocket.send("report4;No Sales for Basic T-shirts.".encode())
                        return

                    # find the color with the maximum return count
                    maxCount = max(colorCounts.values())
                    mostReturnedColors = [color for color, count in colorCounts.items() if count == maxCount]
                    self.clientSocket.send(f"report4;{','.join(mostReturnedColors)}".encode())

                except Exception as e:
                    print(f"Error processing report4: {e}")
                    self.clientSocket.send("report4error;Server error occurred.".encode())

            # Invalid report code
            else:
                self.clientSocket.send(f"{reportCode}error;Invalid report code.".encode())

        except Exception as e:
            print(f"Error processing report {reportCode}: {e}")
            self.clientSocket.send(f"{reportCode}error;Server error occurred.".encode())

    # This helper function retrieves the price of a specific item based on its ID and color from `items.txt`.
    # It scans the file for a matching entry and returns the price.
    # If the item is not found, it returns 0 by default.

    def getPrice(self, itemID, color):
        try:
            with fileLock, open("items.txt", "r") as itemsFile:
                for line in itemsFile:
                    fileItemID, itemName, itemColor, price, stock = line.strip().split(";")
                    if fileItemID == itemID and itemColor == color:
                        return int(price)
        except Exception as e:
            print(f"Error retrieving price for {itemID}-{color}: {e}")
        return 0  # Default price if not found

    # This function processes a purchase operation from the client.
    # It validates each item in the purchase request to ensure there’s enough stock and calculates the total cost.
    # If any item is unavailable or not found, it sends an error message to the client.
    # If all items are available, it updates `items.txt` with the reduced stock, logs the purchase in `operations.txt`,
    # and sends a success message with the total cost to the client.

    def processPurchase(self, store, totalQuantity, itemsList, customerName):
        try:
            itemStock = {}  # dictionary to hold item data for quick access
            unavailableItems = []  # track unavailable items
            totalCost = 0  # total cost of the purchase

            # Load item data from items.txt
            with fileLock, open("items.txt", "r") as itemsFile:
                for line in itemsFile:
                    fileItemID, itemName, itemColor, price, stock = line.strip().split(";")
                    itemStock[(fileItemID, itemColor)] = [itemName, int(price), int(stock)]

            # Validate items in the purchase request
            for item in itemsList:
                quantity, itemID, color = item.split("-")
                quantity = int(quantity)
                key = (itemID, color)

                if key in itemStock:
                    itemName, price, stock = itemStock[key]
                    if stock >= quantity:
                        # Stock is sufficient, calculate cost
                        totalCost += price * quantity
                    else:
                        # Stock insufficient
                        unavailableItems.append(f"{itemName}-{color} (requested: {quantity}, available: {stock})")
                else:
                    # Item not found
                    unavailableItems.append(f"{itemID}-{color} not found")

            # If there are unavailable items, respond with an error and exit
            if unavailableItems:
                self.clientSocket.send(f"availabilityerror;{','.join(unavailableItems)}".encode())
                return

            #issue here!!!
            for item in itemsList:
                quantity, itemID, color = item.split("-")
                quantity = int(quantity)
                key = (itemID, color)

                if key in itemStock:
                    itemStock[key][2] -= quantity  # Deduct stock

            with fileLock, open("items.txt", "w") as itemsFile:
                for key, (itemName, price, stock) in itemStock.items():
                    fileItemID, itemColor = key
                    itemsFile.write(f"{fileItemID};{itemName};{itemColor};{price};{stock}\n")

            # log the purchase operation in operations.txt
            with fileLock, open("operations.txt", "a") as operationsFile:
                operationsFile.write(f"purchase;{store};{customerName};{','.join(itemsList)}\n")

            # notify the client of success and total cost
            self.clientSocket.send(f"purchasesuccess;{totalCost}".encode())

        except Exception as e:
            print(f"Error during purchase operation: {e}")
            self.clientSocket.send("purchaserror;Server error occurred.".encode())

    # This function processes a return operation from the client.
    # It checks if the items being returned were purchased by the customer and have not been returned before.
    # If valid, it updates `items.txt` with the incremented stock and logs the return in `operations.txt`.
    # If any item is invalid for return, it sends an error message to the client.
    # A success message is sent when the return is processed without issues.

    def processReturn(self, store, totalQuantity, itemsList, customerName):
        try:
            itemStock = {}
            alreadyReturnedItems = []
            validReturn = True

            with fileLock, open("items.txt", "r") as itemsFile:
                for line in itemsFile:
                    fileItemID, itemName, itemColor, price, stock = line.strip().split(";")
                    itemStock[(fileItemID, itemColor)] = [itemName, int(price), int(stock)]

            with fileLock, open("operations.txt", "r") as operationsFile:
                purchaseRecords = operationsFile.readlines()

            for item in itemsList:
                quantity, itemID, color = item.split("-")
                quantity = int(quantity)
                key = (itemID, color)

                if not any(f"{itemID}-{quantity}-{color}" in record and "purchase" in record for record in
                           purchaseRecords):
                    validReturn = False
                    alreadyReturnedItems.append(f"{itemID}-{color} not valid for return")
                else:
                    if key in itemStock:
                        itemStock[key][2] += quantity  # Increment stock

            if not validReturn:
                self.clientSocket.send(f"returnerror;{' '.join(alreadyReturnedItems)}".encode())
                return

            with fileLock, open("items.txt", "w") as itemsFile:
                for key, (itemName, price, stock) in itemStock.items():
                    fileItemID, itemColor = key
                    itemsFile.write(f"{fileItemID};{itemName};{itemColor};{price};{stock}\n")

            with fileLock, open("operations.txt", "a") as operationsFile:
                operationsFile.write(f"return;{store};{customerName};{','.join(itemsList)}\n")

            self.clientSocket.send("returnsuccess".encode())

        except Exception as e:
            print(f"Error during return operation: {e}")
            self.clientSocket.send("returnerror;Server error occurred.".encode())


# Main server setup
if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("Server is running and waiting for connections...")

    while True:
        serverSocket.listen()
        clientSocket, clientAddress = serverSocket.accept()
        clientThread = ClientThread(clientSocket, clientAddress)
        clientThread.start()
