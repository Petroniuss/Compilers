from operator import itemgetter

# We're going to employ visitor pattern to visit nodes


class Ast:
    def __init__(self, type, children=None):
        self.type = type
        if children is None:
            self.children = []
        else:
            self.children = children

    def __str__(self):
        return str(self.type)


class BinaryExpression(Ast):
    def __init__(self, operator, leftOperand, rightOperand):
        super().__init__(operator,
                         children=[leftOperand, rightOperand])
        self.operator = operator

    def leftOperand(self):
        return self.children[0]

    def rightOperand(self):
        return self.children[1]


class FunctionCall(Ast):
    def __init__(self, name, argList):
        super().__init__('FunctionCall', children=argList)
        self.name = name


class Vector(Ast):
    def __init__(self, elements):
        super().__init__('Vector', children=elements)

    def append(self, e):
        self.children.append(e)

    def __str__(self):
        return str(self.children)


class Identifier(Ast):
    def __init__(self, id):
        super().__init__('ID')
        self.id = id

    def __str__(self):
        return f'{self.type} : {self.id}'


class Primitive(Ast):
    def __init__(self, type, value):
        super().__init__(type)
        self.value = value

    def __str__(self):
        return f'{self.type} : {self.value}'

    def __repr__(self):
        return self.__str__()


def String(value):
    return Primitive('String', value)


def Int(value):
    return Primitive('Int', value)


def Float(value):
    return Primitive('Float', value)


def emptyVector():
    return Vector([])
