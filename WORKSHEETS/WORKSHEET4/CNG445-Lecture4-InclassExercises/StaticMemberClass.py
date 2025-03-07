
class StaticMemberClass:
    x = 0 # static attribute

    @staticmethod
    def Smethod():
        return StaticMemberClass.x > 2
    def __init__(self):
        self.c = 5
        StaticMemberClass.x = StaticMemberClass.x + 1

if __name__ == "__main__":
    a = StaticMemberClass()
    print(a.Smethod())
    b = StaticMemberClass()
    print(b.Smethod())
    c = StaticMemberClass()
    print(c.Smethod())
    print(StaticMemberClass.Smethod())

    c.x = 10
    print(c.x)
    print(StaticMemberClass.x)
