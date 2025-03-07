from socket import *
from threading import *
import sqlite3

# Lock for thread synchronization
fileLock = RLock()

# This is the constructor for the `ClientThread` class.
# It initializes the thread for each connected client and sets up their socket and address.
# Also, it prints a message confirming that a new client is connected.

class ClientThread(Thread):
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self)
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
                if clientMessage.startswith("GetCourse;"):
                    self.handleCourse(clientMessage)


                # Invalid command handling
                else:
                    print(f"Invalid command received: {clientMessage}")
                    self.clientSocket.send("Invalid command.".encode())

        except Exception as error:
            print(f"Error with client {self.clientAddress}: {error}")
        finally:
            self.clientSocket.close()
            print(f"Connection closed with {self.clientAddress}")


    def handleCourse(self,clientMessage):
        _,year,semester,multiplecorse= clientMessage.strip().split(";")
        coursesfound= []
        academicsemester=year+semester
        try:
            # Connect to the database
            conn = sqlite3.connect("department.db")
            cursor = conn.cursor()
            if multiplecorse:
                cursor.execute("SELECT coursecode  FROM courselecturer WHERE academicsemester = ?", (academicsemester,))
            else:
                pass
            result=cursor.fetchone()
            if result: #that means we found a course and we should send the name of the courses with sections in comma between
                pass # assuming we found the courses => coursesfound.append(course) while we still have courses, and we need count for the sections, then we send the message to the client in the format needed using ";".join()

            else: #we didn't find the course
                clientSocket.send("nocourse".encode())
        finally:
            conn.close()


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