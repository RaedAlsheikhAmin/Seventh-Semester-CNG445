class Test:

    def __init__(self):
        self._a = 20
        self.__b = 30

if __name__ == "__main__":
    t = Test()
    print(t._a)
    #print(t.__b)
    print(t._Test__b)