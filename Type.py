class Type:
    def __init__(self):
        super().__init__()

    def type(self):
        return unitType()


class Primitive(Type):
    """
        Primitive type like 'int'
    """

    def __init__(self, t: str):
        self.t = t

    def type(self):
        return self.t


class Arrow(Type):
    """
        t -> tNext 

        tNext can either be an arrow or primitive type.
    """

    def __init__(self, t: str, tNext: Type):
        super().__init__()
        self.t = t
        self.tNext = tNext

    def type(self):
        return self.t + ' -> ' + self.tNext.type()

    def apply(self):
        """
            Returns type after application of first argument.
        """
        return self.tNext


def typecheck(t1: Type, t2: Type):
    """
        Since we don't allow any polymorphism this is simple..
    """
    return t1.type() == t2.type()


def intType():
    return 'Int'


def stringType():
    return 'String'


def floatType():
    return 'Float'


def unitType():
    return 'Unit'
