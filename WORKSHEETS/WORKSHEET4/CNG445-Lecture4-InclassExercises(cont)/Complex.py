class Complex:

    def __init__(self, r=1, i=1):
        self.real = r
        self.imag = i

    def __str__(self):
        return "({}, {} i)".format(self.real, self.imag)
        #return f"{self.real},{self.imag} i"

    def __add__(self, other):
        realpart = self.real + other.real
        imagpart = self.imag + other.imag
        return Complex(realpart, imagpart)

    def __sub__(self, other):
        realpart = self.real - other.real
        imagpart = self.imag - other.imag
        return Complex(realpart, imagpart)

if __name__ == "__main__":
    c1 = Complex(5,5)
    c2 = Complex(4,4)
    c3 = c1 + c2
    print(c3)
    c4 = c1-c2
    print(c4)