try:
    file= open("clients.txt", "w")
except IOError:
    print("File can not be opened")
    exit(1)
print("Enter the account, name, and balance: ")
for i in range(0,3):
    accountLine=input("? ")
    file.write(accountLine + "\n")

file.close()


