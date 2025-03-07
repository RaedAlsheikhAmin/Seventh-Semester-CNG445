from socket import *

SERVER = "127.0.0.1"
PORT = 5000

client = socket(AF_INET, SOCK_STREAM)
client.connect((SERVER, PORT))

while True:
    in_data = client.recv(1024).decode()
    print("From server: " + in_data)
    out_data = input("Enter your question: ")
    client.send(out_data.encode())
    if out_data == "bye":
        break
client.close()

