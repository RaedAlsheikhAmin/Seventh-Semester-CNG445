import pickle

from Time import *
t = Time(2,3,4)
print(t)
t.hour = 24
t.minute = 10
t.second = 50
#t.extra = 100
print(t)

print(t._hour)
print(t._sec)

with open("myfile.txt", "wb") as binary_file:
    byte_rep = pickle.dumps(t)
    binary_file.write(byte_rep)
