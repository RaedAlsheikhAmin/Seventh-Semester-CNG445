class Container:

    #def __init__(self, content = []):
    #    self.content = content

    def __init__(self):
        self.content = []
        
    def printContent(self):
        print(self.content)

if __name__ == "__main__":
    item1 = Container()
    item1.content.append(1)
    item1.content.append(2)

    item2 = Container()
    item2.content.append(3)
    item2.content.append(4)

    item1.printContent()
    item2.printContent()