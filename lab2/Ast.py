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


class For(Ast):
    def __init__(self, id, beginExpr, endExpr):
        super().__init__('For', children=[id, beginExpr, endExpr])

    def id(self):
        return self.children[0]

    def beginExpr(self):
        return self.children[1]

    def endExpr(self):
        return self.children[2]


class While(Ast):
    def __init__(self, condition, block):
        super().__init__('Break', children=[condition, block])

    def condition(self):
        return self.children[0]

    def block(self):
        return self.children[1]


class Break(Ast):
    def __init__(self):
        super().__init__('Break')


class Continue(Ast):
    def __init__(self):
        super().__init__('Continue')


class Return(Ast):
    def __init__(self, expression):
        super().__init__('Return', children=[expression])


class FunctionCall(Ast):
    """
        there are few already mentioned:
            - transpose (matrix transpose)
            - negative (numerical negative)
            - zeros
            - ones
    """

    def __init__(self, functionname, arglist):
        super().__init__('FunctionCall', children=arglist)
        self.functionname = functionname


class ObjectFunctionCall(Ast):
    def __init__(self, objOrId, functionName, argList):
        super().__init__('ObjectFunctionCall', children=[objOrId] + argList)
        self.functionName = functionName

    def objectOrId(self):
        return self.children[0]

    def args(self):
        return self.children[1:]


class Vector(Ast):
    def __init__(self, elements):
        super().__init__('Vector', children=elements)

    def __str__(self):
        return str(self.children)


class Slice(Ast):
    def __init__(self, ranges):
        super().__init__('Slice', children=ranges)


class Condition(Ast):
    def __init__(self, expression):
        super().__init__('Condition', children=[expression])

    def body(self):
        return self.children[0]


class RelationalExp(Ast):
    def __init__(self, operator, left, right):
        super().__init__(operator, children=[left, right])

    def operator(self):
        return self.type

    def left(self):
        return self.children[0]

    def right(self):
        return self.children[1]


class Bind(Ast):
    def __init__(self, id, assignOperator, expression):
        super().__init__(assignOperator, children=[id, expression])

    def id(self):
        return self.children[0]

    def expression(self):
        return self.children[1]


class BindWithSlice(Ast):
    def __init__(self, id, slice, assignOperator, expression):
        super().__init__(assignOperator, children=[id, slice, expression])

    def id(self):
        return self.children[0]

    def slice(self):
        return self.children[1]

    def expression(self):
        return self.children[2]


class BinaryOp(Ast):
    def __init__(self, operator, left, right):
        super().__init__(operator, children=[left, right])

    def operator(self):
        return self.type

    def left(self):
        return self.children[0]

    def right(self):
        return self.children[1]


class If(Ast):
    def __init__(self, condition, trueBlock):
        super().__init__('If', children=[condition, trueBlock])

    def condition(self):
        return self.children[0]

    def trueBlock(self):
        return self.children[1]


class IfElse(Ast):
    def __init__(self, condition, trueBlock, falseBlock):
        super().__init__('IfElse', children=[condition, trueBlock, falseBlock])

    def condition(self):
        return self.children[0]

    def trueBlock(self):
        return self.children[1]

    def falseBlock(self):
        return self.children[2]


class Identifier(Ast):
    def __init__(self, id):
        super().__init__('ID', children=[id])

    def id(self):
        return self.children[0]

    def __str__(self):
        return f'{self.type} : {self.id}'


class Primitive(Ast):
    """
        We might wanna create separate class for each primitive but for now this works.
    """

    def __init__(self, type, value):
        super().__init__(type)
        self.value = value

    def __str__(self):
        return f'{self.type} : {self.value}'

    def __repr__(self):
        return self.__str__()


class CodeBlock(Ast):
    def __init__(self, statements):
        super().__init__('CodeBlock')

        self.statements = statements


def String(value):
    return Primitive(stringType(), value)


def Int(value):
    return Primitive(intType(), value)


def Float(value):
    return Primitive(floatType(), value)


def intType():
    return 'Int'


def stringType():
    return 'String'


def floatType():
    return 'Float'


def emptyVector():
    return Vector([])
