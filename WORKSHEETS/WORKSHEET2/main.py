#worksheet 2
#question 1 and 2 are solved on paper
#question 3 is homework
#question 4 is solved on paper

#question 5
sentence= input("give me a sentence: ")
sentence=" ".join([i[0].upper()+ i[1:] for i in sentence.split(' ')])
print(sentence)



#question 6
sentence6=input("Enter a sentence: ")
d={}
sentence6= sentence6.upper()
for s in sentence6:
    if s in d.keys():
        d[s] +=1
    else:
        d[s]=1

print(d)



#question 7 homework
