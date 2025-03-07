try:
    file= open("clients.txt", "r")
except IOError:
    print("File couldn't be opened")
    exit(1)

#first way of reading it
#records= file.readlines()
#print(records)

#second way of reading
records=file.read().split("\n")
print(records)

file.close()