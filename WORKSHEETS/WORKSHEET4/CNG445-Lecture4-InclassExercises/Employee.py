
class Employee:

    def __init__(self, first, last):
        #if self.__class__ == Employee:
        #    raise NotImplementedError("This is an abstact class")
        self.firstname = first
        self.lastname = last

    def __str__(self):
        return self.firstname + " " + self.lastname

class HourlyEmployee(Employee):

    def __init__(self, first, last, hour, hourlywage):
        Employee.__init__(self, first, last)
        self.hour = hour
        self.hourlywage = hourlywage

    def computeWage(self):
        return self.hourlywage * self.hour

if __name__ == "__main__":
    e = Employee("Sukru", "Eraslan")
    print(e)
    e2 = HourlyEmployee("Adam", "Mohamed", 10, 20)
    print(e2)
    print(e2.computeWage())

    print(issubclass(HourlyEmployee, Employee))
    print(isinstance(e, Employee))
    print(isinstance(e2, HourlyEmployee))
    print(isinstance(e2, Employee))
    print(isinstance(e, HourlyEmployee))


