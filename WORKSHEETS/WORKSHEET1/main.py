#worksheet 1

#question 1
a_str = "acd"
print(a_str[1])
#no problem here
a_str = "acd"
a_str[1] = 'b'
print(a_str)
#strings are immutable => they can not be changed

a_list = [1,3,2,4]
a_list[1] = 2
print(a_list)

#strings can not be changed, but lists can.

#question 2
row1=["H","He"]
row2=["Li","Be","F","Ar"]
row3=["Na","Mg","Cl","Ne"]
ptable=row1
ptable.extend(row2)
ptable.extend(row3)

#a. What is the value of ptable now?

#all the rows

#b. What is the value of row1 now? Is this what you expected?

#it is like ptable => all of them

#c. Correct the error in row2 (Ar should be Ne) by executing a command of the form row2[?] = ?.

#row2[3] ="Ne"

#What happens to ptable as a result of this assignment?

#no changes


#d. Correct the error in row3 (Ne should be Ar) by executing a command of the form ptable[?] = ?.

#ptable[-1]="Ar"

#What happens to row3 as a result of this assignment?

#nothing happens

#question 3

#3. The following code attempts to construct a table containing the first three rows of the periodic table. Run the following commands in Python:
row1 = ["H","He"]
row2 = ["Li","Be","F","Ar"]
row3 = ["Na","Mg","Cl","Ne"]
ptable = [row1]
ptable.append(row2)
ptable.append(row3)
#a. What is the value of ptable now? How does this differ from what you had in Exercise 2?
#[[row1],[row2],[row3]]

#b. What is the value of row1 now? How does it differ from what you had in Exercise 2?
#it is not changed => because ptable is the main thing here

#c. Correct the error in row 2 (Ar should be Ne) by executing a command of the form row2[?] = ?.#Does this also change ptable?
#row2[3]= "Ne"


#d. Correct the error in row 3 (Ne should be Ar) by executing a command of the form ptable[?][?] =?.#Does this change row3?

#ptable[2][3]="Ar"

