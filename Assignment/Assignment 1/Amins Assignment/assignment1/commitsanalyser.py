
# =====================
# STEP 1
# importing the relevant modules
# =====================
import matplotlib.pyplot as plt
import sys
# =====================

# =====================
# STEP 2
# opening identities.txt
# 'names' list
#   it is going to store the names and surnames of the users
# 'dict' dictionary
#   it stores name_surname, SWM, NFR, and SoftEvol
# 'aux_dict' dictionary
#   it stores data from identities.txt
# 'identities_lines'
#   it uses 'readlines' method in order to read each line except first one
#   since the column is not part of the data
# =====================
f = open(sys.argv[2], "r")
names = []  # Empty list for names_surnames
dict = {}  # Dictionary(Nested) for name_surname and SWM,NFR,SoftEvol
aux_dict = {}  # Auxiliary dictionary for storing data from identities.txt
identities_lines = f.readlines()[1:]  # Takes the list starting from the first name
f.close()
# =====================

# =====================
# STEP 3
# reading the contents of identities.txt
#   the code reads the contents of identities.txt by iterating through each line
#   that was read in STEP 2
# the loop ensures that the same person (the same name_surname combination) with
# different id is also considered
# =====================
for line in identities_lines:
    name_surname = line.split(",")[1]  # Equals to name_surname string
    if names.count(name_surname) == 0:  # If there is no such name_surname combination in the list it adds it to the list
        names.append(name_surname)
    id = line.split(",")[0]  # Equals to id of the user
    id = int(id)
    aux_dict[id] = name_surname  # Aux dict takes id as key and stores name_surname as value, this is important
    # since a person can have different id's
# =====================

# =====================
# STEP 4
# The loop for initializing each item in the dictionary
#   The dictionary will be initialized to zero values in order to
#   modify them in the next step
# Also, reading commits.txt file and reading everything except the first line
# since the first line does not contain the data that needs to be considered
# =====================
for i in range(0, len(names)):  # Initializes each dict item
    dict[names[i]] = {}
    dict[names[i]]['SWM'] = [0, 0, 0]
    dict[names[i]]['NFR'] = [0, 0, 0, 0, 0, 0]
    dict[names[i]]['SoftEvol'] = [0, 0, 0, 0]
f = open(sys.argv[1], "r")
commit_lines = f.readlines()[1:]
f.close()
# =====================

# =====================
# STEP 5
# The loop that reads and analyzes the data from commits.txt file contents
# read in STEP 4
# zip() function along with list comprehension were used in order to properly
# read the github commits for each user
# =====================
for i in commit_lines:
    user_id = i.split(",")[14]  # Equals to user id
    user_id = int(user_id)
    SWM = i.split(",")[1:4]  # Equals to the swm values
    NFR = i.split(",")[4:10]  # Equals to the nfr values
    SoftEvol = i.split(",")[10:14]  # Equals to the softevol values
    SWM = [int(x) for x in SWM]  # Turns string list into integer list
    NFR = [int(x) for x in NFR]
    SoftEvol = [int(x) for x in SoftEvol]
    dict[aux_dict[user_id]]['SWM'] = [x + y for x, y in zip(dict[aux_dict[user_id]]['SWM'], SWM)]  # Adds each line
    # to the proper user one by one
    dict[aux_dict[user_id]]['NFR'] = [x + y for x, y in zip(dict[aux_dict[user_id]]['NFR'], NFR)]
    dict[aux_dict[user_id]]['SoftEvol'] = [x + y for x, y in zip(dict[aux_dict[user_id]]['SoftEvol'], SoftEvol)]
# =====================

# =====================
# STEP 6
# The main loop that controls the entire program
# =====================
while True:
    print("1-)Compare the number of commits done by a particular developer for a given classification scheme")
    print("2-)Compare the number of commits done by all developers, which are classified with a given "
          "feature.")
    print("3-)Print the developer with the maximum number of commits for a given feature")
    print("4-)Exit")
    try:
        x = int(input())
    except ValueError:
        x = -1  # to send it to case_ and tell user the input is not correct
    match x:
        # =====================
        # case 1 - if the user chose the first option
        # =====================
        case 1:
            # =====================
            # loop 1.1 - for printing out each user that created a commit
            # =====================
            while True:
                print("Which commiter will you chose?")
                c = 1
                for i in dict:
                    print(str(c) + ".-)" + i)
                    c += 1
                try:
                    choice = int(input())
                except ValueError:
                    choice = -1
                if len(dict) >= choice > 0:
                    break
                else:
                    print("Write a proper number!")
            commiter = list(dict.keys())[choice - 1]
            print(commiter)
            # =====================

            # =====================
            # loop 1.2 - simply for asking a classification scheme and ensuring
            # the input i correct
            # =====================
            while True:
                print("Select a classification scheme:\n1-)Swanson's Maintenance Tasks\n"
                      "2-)NFR Labelling\n3-)Software Evolution")
                try:
                    choice = int(input())
                except ValueError:
                    choice = -1
                if 3 >= choice > 0:
                    break
                else:
                    print("Write a proper number!")
            # =====================

            # =====================
            # this piece of code identifies which data the user wants to see
            # and creates a bar graph with correct title and features
            # then, it creates the labels for x and y and also changes
            # the rotation to 30 degrees and fontsize to 10 for readability
            # =====================
            if choice == 1:
                features = ["Corrective Tasks", "Adaptive Tasks", "Perfective Tasks"]
                plt.bar(features, dict[commiter]["SWM"])
                plt.title("Comparison for" + str(commiter) + "\'s Commits Classified by SwM Tasks")
            elif choice == 2:
                features = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
                plt.bar(features, dict[commiter]["NFR"])
                plt.title("Comparison for" + str(commiter) + "\'s Commits Classified by NFR Labelling")
            elif choice == 3:
                features = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
                plt.bar(features, dict[commiter]["SoftEvol"])
                plt.title("Comparison for" + str(commiter) + "\'s Commits Classified by Software evalution tasks")
            plt.xlabel('Features')
            plt.xticks(rotation=30, fontsize=10)
            plt.ylabel('Total Number of Commits')

            plt.show()
            # =====================

        # =====================
        # case 2 - if the user chose the second option
        # =====================
        case 2:
            # =====================
            # loop 2.1 - simply for asking a classification scheme and ensuring
            # the input is correct
            # =====================
            while True:
                print("Select a classification scheme:\n1-)Swanson's Maintenance Tasks\n"
                      "2-)NFR Labelling\n3-)Software Evolution")
                try:
                    choice = int(input())
                except ValueError:
                    choice = -1
                if 3 >= choice > 0:
                    break
                else:
                    print("Write a proper number!")
            # =====================

            # =====================
            # if-else chain that shows the comparison based on classification
            # scheme choice of the user
            # =====================
            if choice == 1:
                # =====================
                # loop 2.2 - simply for asking a type of task the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Corrective Tasks", "\n2-)Adaptive Tasks", "\n3-)Perfective Tasks")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 3 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================

                features = []
                values = []
                for i in dict:
                    features.append(i)
                    values.append(dict[i]["SWM"][choice-1])

                plt.bar(features, values)
                plt.xlabel('Feature')
                plt.xticks(rotation=30, fontsize=10)
                plt.ylabel('Number of Commit')
                plt.title('Comparison for Specific task in SWM')
                plt.show()

            elif choice == 2:
                # =====================
                # loop 2.3 - simply for asking a part of data the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Maintainability\n"
                          "2-)Usability\n"
                          "3-)Functionality\n"
                          "4-)Reliability\n"
                          "5-)Efficiency\n"
                          "6-)Portability")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 6 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================
                features = []
                values = []
                for i in dict:
                    features.append(i)
                    values.append(dict[i]["NFR"][choice-1])

                plt.bar(features, values)
                plt.xlabel('Feature')
                plt.xticks(rotation=30, fontsize=10)
                plt.ylabel('Total Number of Commits')
                plt.title('Comparison for specific feature in NFR')
                plt.show()
            elif choice == 3:
                # =====================
                # loop 2.4 - simply for asking a part of data the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Forward Engineering,\n2-)Re-Engineering,\n3-)Corrective Engineering,\n4-)Management.")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 4 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================
                features = []
                values = []
                for i in dict:
                    features.append(i)
                    values.append(dict[i]["SoftEvol"][choice-1])

                plt.bar(features, values)
                plt.xlabel('Feature')
                plt.xticks(rotation=30, fontsize=10)
                plt.ylabel('Total Number of Commits')
                plt.title('Comparison for specific feature in SoftEvol')
                plt.show()
            # =====================

        # =====================
        # case 3 - if the user chose the third option
        # =====================
        case 3:
            # =====================
            # loop 3.1 - simply for asking a classification scheme the user wants to see
            # and ensuring the input is correct
            # =====================
            while True:
                print("Select a classification scheme:\n1-)Swanson's Maintenance Tasks\n"
                      "2-)NFR Labelling\n3-)Software Evolution")
                try:
                    choice = int(input())
                except ValueError:
                    choice = -1
                if 3 >= choice > 0:
                    break
                else:
                    print("Write a proper number!")
            # =====================

            # =====================
            # if-else chain that prints the maximum number of commits for
            # a particular user and asks which type of data the user wants to see
            # =====================
            if choice == 1:
                # =====================
                # loop 3.2 - simply for asking a type of tasks the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Corrective Tasks", "\n2-)Adaptive Tasks", "\n3-)Perfective Tasks")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 3 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================
                max = 0
                counter = 1
                num = 0
                for i in dict:
                    if dict[i]["SWM"][choice-1]>max:
                        max = dict[i]["SWM"][choice-1]
                        num = counter
                    counter += 1
                print("Maximum number owner is "+str(list(dict.keys())[num]))

            elif choice == 2:
                # =====================
                # loop 3.3 - simply for asking a part of data the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Maintainability\n2-)Usability\n3-)Functionality\n"
                          "4-)Reliability\n5-)Efficiency\n6-)Portability")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 6 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================
                max = 0
                counter = 1
                num = 0
                for i in dict:
                    if dict[i]["NFR"][choice - 1] > max:
                        max = dict[i]["NFR"][choice - 1]
                        num = counter
                    counter += 1
                print("Maximum number owner is "+str(list(dict.keys())[num]))
            elif choice == 3:
                # =====================
                # loop 3.4 - simply for asking a part of data the user wants to see
                # and ensuring the input is correct
                # =====================
                while True:
                    print("1-)Forward Engineering,\n2-)Re-Engineering,\n3-)Corrective Engineering,\n4-)Management.")
                    try:
                        choice = int(input())
                    except ValueError:
                        choice = -1
                    if 4 >= choice > 0:
                        break
                    else:
                        print("Write a proper number!")
                # =====================
                max = 0
                counter = 0
                num = 0
                for i in dict:
                    if dict[i]["SoftEvol"][choice - 1] > max:
                        max = dict[i]["SoftEvol"][choice - 1]
                        num = counter
                    counter += 1
                print("Maximum number owner is " + str(list(dict.keys())[num]))
        # =====================

        # =====================
        # case 4 - if the user wants to exit thew application
        # =====================
        case 4:
            exit()
        # =====================

        # =====================
        # any other case - if the user writes the improper value
        # =====================
        case _:
            print("Please write a proper value(1-4)!")
        # =====================
# =====================
