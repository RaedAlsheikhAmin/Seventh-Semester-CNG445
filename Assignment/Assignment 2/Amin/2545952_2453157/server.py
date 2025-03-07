import socket
import threading
import datetime as dt

# Constants 
# ===================================
PORT = 5000
SERVER = "127.0.0.1"

ADDR = (SERVER, PORT)

DISCONNECT_MESSAGE = "WINDOWCLOSE"
# ===================================

# Creating a socket and binding it to the server
# ===================================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
# ===================================

# Opening the files
# strip() is used to eliminate '\n' symbols when using readlines() method
# ===================================
with open("users.txt") as file:
  users = [user.strip() for user in file.readlines()]
  
with open("books.txt") as file:
  books = [book.strip() for book in file.readlines()]
  
with open("operations.txt") as file:
  operations = [operation.strip() for operation in file.readlines()]
# ===================================


# handle_client() function is activated for each new client that connects to the server
# ===================================
def handle_client(conn, addr):
  # ===================================
  # line (71)
  #   taking the global values of operations and books because 
  #   after client rents or returns a book, the operations.txt
  #   and books.txt files are changed, so the program reads them 
  #   again and stores them into existing variables
  # line (73)
  #   USERNAME is used to store the username of librarian because
  #   we need to store it each time a book is rented
  # 
  # lines(79 - 318) main if-else chain to control the type of operations
  #   if operation_type is login
  #     server handles the login functionality by comparing username and
  #     password entered with users.txt file data
  
  #   elif operation_type is rent
  #     the client can send more than 1 book id to the server, so the main
  #     strategy here is looping through list of books and saving the ones
  #     with the correct ids. Further functionality is explained between
  #     in the statement itself
  
  #   elif operation_type is return
  #     checking whether the person has returned a book
  #       This is done by counting the number of return and rent 
  #       for the same book id and person's name.
  #       If there is one "rent" operation WITHOUT corresponding
  #       "return" operation, the person is allowed to return that book.
  
  #  elif operation_type is report
  #    this is a big statement that controls each type of report
  #    the manager wants to get (1,2,3,4).
  
  # ===================================
  global operations, books
  
  USERNAME = ""
  while True:
    msg = conn.recv(1024).decode("utf-8")
    
    operation_type = msg.split(";")[0]

    if operation_type == "login":
      success = False
      for user in users:
        if msg.split(";")[1] == user.split(";")[0] and msg.split(";")[2] == user.split(";")[1]:
          conn.send(f"loginsuccess;{user.split(';')[0]};{user.split(';')[2]}".encode("utf-8"))
          USERNAME = user.split(';')[0]
          success = True
      if not success:
        conn.send("loginfailure".encode("utf-8"))
    elif operation_type == "rent":
      
      # storing all ids that the client sent
      ids = [item for item in msg.split(";")[4:]]
      
      # this will be set to false to send availabilityerror
      available = True
      
      for id in ids:
        for book in books:
          if id == book.split(";")[0] and int(book.split(";")[-1]) <= 0:
            available = False
          # book.split()[0] is id of the book.
          # book.split()[-1] is the number of copies available.
          # if number of copies is 0, the book is not available.
      
      # if the book is not available
      if not available:
        conn.send(f"availabilityerror".encode("utf-8"))
        continue
      
      # if the user has not returned all books he/she rented
      if operations:
        user_operations = [operation.split(";")[0] for operation in operations if operation.split(";")[2] == msg.split(";")[2]]
        if not user_operations.count("rent") == user_operations.count("return"):
          conn.send(f"renterror".encode("utf-8"))
          continue
      
      # If none of erros was thrown, the server creates an operation for EACH of
      # ids sent by the client. 
      # It then appends new operation to operations.txt file and updates books.txt
      # file with updated availability
      for id in ids:
        for book in books:
          if id == book.split(';')[0]:
            books_cost = book.split(';')[-2]
        operation = f"rent;{USERNAME};{msg.split(';')[2]};{msg.split(';')[3]};{books_cost};{id}"
        with open("operations.txt", "a") as file:
          file.write(f"{operation}\n")
      with open("books.txt", "w") as file:
        for book in books:
          found = 0
          for id in ids:
            if id == book.split(';')[0]:
              file.write(f"{book.split(';')[0]};{book.split(';')[1]};{book.split(';')[2]};{book.split(';')[3]};{int(book.split(';')[4]) - 1}\n")
              found = 1
              break
          if found == 0:
            file.write(f"{book}\n")
            
      # the contents of files changed, so the server reads them again
      with open("books.txt") as file:
        books = [book.strip() for book in file.readlines()]
        
      with open("operations.txt") as file:
        operations = [operation.strip() for operation in file.readlines()]
        
      conn.send("rentsuccess".encode("utf-8"))
    
    elif operation_type == "return":
      # total cost to be sent BACK TO CLIENT
      total_cost = 0
      
      # storing all ids that the client sent
      ids = [item for item in msg.split(";")[4:]]
      
      # operations list which is going to store return operations.
      # (one return operation for every returned book).
      operations_to_store = []
      
      # we need to make sure that the person actually rented the book that
      # he/she wants to return. This is why for every return operation to
      # be done, there MUST be rent operation with the same name and the
      # the same book.
      # the other condition to check is that the user has not returned
      # the same book already.
      # terminate operation controls the process of checking these 2 conditions.
      terminate_operation = False
      
      for operation in operations:
        if operation.split(';')[2] == msg.split(';')[2] and operation.split(';')[0] == "rent" and operation.split(';')[-1] in ids:
          
          for operation_ in operations:
            if operation_.split(';')[2] == msg.split(';')[2] and operation_.split(';')[0] == "return" and operation_.split(';')[-1] in ids:
              terminate_operation = True
              break
          if terminate_operation:
            terminate_operation = False
            continue
          
          # removing the id of the book that was rent and returned successfully
          ids.remove(operation.split(';')[-1])
          
          return_date = dt.datetime(int(msg.split(';')[3].split('.')[2]), 
                                    int(msg.split(';')[3].split('.')[1]), 
                                    int(msg.split(';')[3].split('.')[0]))
          rent_date = dt.datetime(int(operation.split(';')[3].split('.')[2]),
                                  int(operation.split(';')[3].split('.')[1]),
                                  int(operation.split(';')[3].split('.')[0]))
          days_between_rent_and_return = (return_date - rent_date).days
          
          cost = float(operation.split(';')[-2]) * days_between_rent_and_return
          total_cost += cost
          
          operation_to_store = f"return;{USERNAME};{msg.split(';')[2]};{msg.split(';')[3]};{cost};{operation.split(';')[-1]}"
          
          operations_to_store.append(operation_to_store)
      
      # if ids list is empty, this means that every book id that
      # was sent by the client has to be returned.
      # if there is at least one id remaining in ids list, the
      # book that the person wants to return was actually returned before.
      if ids == []:
        with open("operations.txt", "a") as file:
          for operation in operations_to_store:
            file.write(f"{operation}\n")
        with open("books.txt", "w") as file:
          for book in books:
            found = 0
            for operation in operations_to_store:
              if book.split(';')[0] == operation.split(';')[-1]:
                file.write(f"{book.split(';')[0]};{book.split(';')[1]};{book.split(';')[2]};{book.split(';')[3]};{int(book.split(';')[4]) + 1}\n")
                found = 1
                break
            if found == 0:
              file.write(f"{book}\n")
        conn.send(f"returnsuccess;{cost}".encode("utf-8"))
      else:
        conn.send("returnerror".encode("utf-8"))
        
      # contents of files changed so opening the files again
      with open("operations.txt") as file:
        operations = [operation.strip() for operation in file.readlines()]
        
      with open("books.txt") as file:
        books = [book.strip() for book in file.readlines()]
        
    elif "report" in operation_type:
      
      # report1 returns most rented books. If there are two or more most rented books
      # with the same number of rents, both books are returned
      if "1" in operation_type:
        operations_to_check = [operation for operation in operations if operation.split(';')[0] == "rent"]
        books_ids = [operation.split(';')[-1] for operation in operations_to_check]
        
        most_frequent_book_ids = []
        max_occuring_id = 0
        for id in books_ids:
          if max_occuring_id < books_ids.count(id):
            max_occuring_id = books_ids.count(id)
        for id in books_ids:
          if books_ids.count(id) == max_occuring_id:
            most_frequent_book_ids.append(id)
        
        with open("books.txt") as file:
          books = [book.strip() for book in file.readlines()]
          
        message_to_send = "report1;"
        
        for book in books:
          if book.split(';')[0] in most_frequent_book_ids:
            message_to_send += f"{book.split(';')[1]};"
        message_to_send = message_to_send[:-1]
        
        conn.send(message_to_send.encode("utf-8"))
        
      # just like report1, report2 can return multiple librarians in case they have
      # performed equal number of operations.
      elif "2" in operation_type:
        librarians = [operation.split(';')[1] for operation in operations]
        
        most_frequent_librarian = 0
        most_popular_librarians = []
        
        for librarian in librarians:
          if most_frequent_librarian < librarians.count(librarian):
            most_frequent_librarian = librarians.count(librarian)
        for librarian in librarians:
          if librarians.count(librarian) == most_frequent_librarian and librarian not in most_popular_librarians:
            most_popular_librarians.append(librarian)
            
        message_to_send = "report2;"
        for item in most_popular_librarians:
          message_to_send += f"{item};"
        message_to_send = message_to_send[:-1]
        conn.send(message_to_send.encode("utf-8"))
        
      # report3 just takes every return operation from operations.txt and sums up the revenue
      elif "3" in operation_type:
        message_to_send = "report3;"
        message_to_send += f"{sum([float(item.split(';')[4]) for item in operations if item.split(';')[0] == 'return'])}"
        conn.send(message_to_send.encode("utf-8"))
        
      elif "4" in operation_type:
        with open("books.txt") as file:
          books = [book.strip() for book in file.readlines()]
        harry_potter_book_id = [book.split(';')[0] for book in books if book.split(';')[1] == "Harry Potter"][0]
        
        # harry potter will only consider dates when the book was rented AND returned
        # if the book was rented but not returned yet, this date will not be considered
        
        # the average time is calculated as follows : 
        #     for each pair of rent-return dates, their difference will be calculated
        #     next, all those differences (periods of time when the book was in rent)
        #     will be summed up and this number will be divided by number of rent-return pairs
        harry_potter_periods = []
        for operation in operations:
          date_returned = None
          if operation.split(';')[-1] == harry_potter_book_id and operation.split(';')[0] == "rent":
            date_rented = operation.split(';')[-3]
            for operation_ in operations:
              if operation_.split(';')[-1] == harry_potter_book_id and operation_.split(';')[0] == "return" and operation_.split(';')[2] == operation.split(';')[2]:
                date_returned = operation_.split(';')[-3]
            
            if date_returned:
              rent_return_tuple = (dt.datetime(int(date_rented.split('.')[2]),
                                               int(date_rented.split('.')[1]),
                                               int(date_rented.split('.')[0])),
                                   dt.datetime(int(date_returned.split('.')[2]),
                                               int(date_returned.split('.')[1]),
                                               int(date_returned.split('.')[0])))
              harry_potter_periods.append(rent_return_tuple)
        
        average_time_rented = 0
        for period in harry_potter_periods:
          average_time_rented += (period[1] - period[0]).days
        try:
          average_time_rented = average_time_rented / len(harry_potter_periods)
        except ZeroDivisionError:
          average_time_rented = 0
        
        conn.send(f"report4;{average_time_rented}".encode("utf-8"))
    
    elif operation_type == DISCONNECT_MESSAGE:
      break
    
  conn.close()
  
server.listen()

while True:
  conn, addr = server.accept()

  thread = threading.Thread(target=handle_client,
                            args=(conn, addr))
  thread.start()