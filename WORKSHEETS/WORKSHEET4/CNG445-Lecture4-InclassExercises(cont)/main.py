class Class1:
    def m(self):
        print("Class 1-m")
    def d(self):
        print("Class 1-d")

class Class2(Class1):
    def m(self):
        print("Class 2-m")
    def d(self):
        print("Class 2-d")

class Class3(Class1):
    def m(self):
        print("Class 3-m")
    def d(self):
        print("Class 3-d")

class Class4(Class3, Class2):
    def m(self):
        print("Class 4-m")

if __name__ == "__main__":
    c = Class4()
    c.m()
    c.d()
    Class2.d(c)
    Class1.d(c)