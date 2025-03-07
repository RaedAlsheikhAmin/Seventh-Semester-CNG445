from Time import *
import pickle

with open("myfile.txt", "rb") as binary_file:
    byte_rep = binary_file.read()
    time = pickle.loads(byte_rep)
    print(time)
    