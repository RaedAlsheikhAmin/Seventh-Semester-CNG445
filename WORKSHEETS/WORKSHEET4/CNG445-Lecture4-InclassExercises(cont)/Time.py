class Time:
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return "{:02d}:{:02d}:{:02d}".format(self.hour, self.minute, self.second)

    def __setattr__(self, key, value):
        if key == "hour":
            if  0 <= value <= 24:
                self.__dict__[key] = value
            else:
                raise ValueError("Invalid value!")
        elif key == "minute" or key == "second":
            if 0 <= value <= 60:
                self.__dict__[key] = value
            else:
                raise ValueError("Invalid value!")
        else:
            raise AttributeError("No such attribute!")

    def __getattr__(self, item):
        if item == "_hour":
            return self.hour
        elif item == "_min":
            return self.minute
        elif item == "_sec":
            return self.second
        else:
            raise AttributeError("No such attribute!")