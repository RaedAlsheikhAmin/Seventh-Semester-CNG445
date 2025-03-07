import math

class Point:

    def __init__(self, x =0, y = 0):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class Line:

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)

    def getLen(self):
        return math.sqrt((self.p1.x - self.p2.x)**2 + (self.p1.y - self.p2.y)**2)

class LineContainer:

    def __init__(self):
        self.lines = []

    def addLine(self, l):
        self.lines.append(l)

    def getTotalLen(self):
        totalLen = 0
        for line in self.lines:
            totalLen += line.getLen()
        return totalLen

if __name__ == "__main__":
    line1 = Line(0, 0, 0, 5)
    line2 = Line(0, 0, 0, 10)
    linecontainerObject = LineContainer()
    linecontainerObject.addLine(line1)
    linecontainerObject.addLine(line2)
    print(linecontainerObject.getTotalLen())


