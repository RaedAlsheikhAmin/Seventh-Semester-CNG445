class Point:

    __slots__ = ["x", "y"]

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def checkNegative(self):
        if self.x < 0 or self.y < 0:
            return True
        else:
            return False

    def __str__(self):
        return "({},{})".format(self.x, self.y)



