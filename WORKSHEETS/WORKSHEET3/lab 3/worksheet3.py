#question 1
import re
from re import *

#part a
a="s: /home/eraslan/445/2018/prj/project.py"
b=a.split("/")
print(b[-1])


#part b
c=a.split("/")
print(c[1:len(c)-1])


#part c
d="I doon't waaaant to haaave aannny eeexxaaam"
d2= re.sub("a+", "a",d)
print(d2)

#second question
