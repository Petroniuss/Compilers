from treelib import Node, Tree

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

    def show(self):
        tree = Tree()
        tree.create_node(tag=str(self), identifier=1)
        parents = [(1, self.children)]
        nextParents = []

        for i in range(2):
            for (id, children) in parents:
                for child in children:
                    node = tree.create_node(tag=str(child), parent=id)
                    if len(child.children) > 0:
                        nextParents.append((node.identifier, child.children))

            parents = nextParents

        tree.show(line_type="ascii-ex", reverse=False)


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
    def __init__(self, id, initExpr, endExpr, body):
        super().__init__('For', children=[id, initExpr, endExpr, body])

    def id(self):
        return self.children[0]

    def initExpr(self):
        return self.children[1]

    def endExpr(self):
        return self.children[2]

    def body(self):
        return self.children[3]


class While(Ast):
    def __init__(self, condition, block):
        super().__init__('While', children=[condition, block])

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

    def __init__(self, functionName, arglist):
        super().__init__('FunctionCall', children=[
            Leaf(functionName)] + arglist)


class ObjectFunctionCall(Ast):
    def __init__(self, objOrId, functionName, argList):
        super().__init__('ObjectFunctionCall', children=[
            Leaf(functionName), objOrId] + argList)

    def objectOrId(self):
        return self.children[0]

    def args(self):
        return self.children[1:]


class Vector(Ast):
    def __init__(self, elements):
        super().__init__('Vector', children=elements)


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


class Range(Ast):
    def __init__(self, begin, end):
        super().__init__('Range', children=[begin, end])

    def begin(self):
        return self.children[0]

    def end(self):
        return self.children[0]


class StartlessRange(Ast):
    def __init__(self, end):
        super().__init__('StartlessRange', children=[end])

    def end(self):
        return self.children[0]


class EndlessRange(Ast):
    def __init__(self, begin):
        super().__init__('EndlessRange', children=[begin])

    def begin(self):
        return self.children[0]


class SimpleRange(Ast):
    def __init__(self, idx):
        super().__init__('SimpleRange', children=[idx])

    def idx(self):
        return self.children[0]


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
        super().__init__('ID', children=[Leaf(id)])

    def id(self):
        return self.children[0].value


class Primitive(Ast):
    """
        We might wanna create separate class for each primitive but for now this works.
    """

    def __init__(self, type, value):
        super().__init__(type, children=[Leaf(value)])

    def value(self):
        return self.children[0].value


class Leaf(Ast):
    def __init__(self, value):
        super().__init__(value, children=[])

    def value(self):
        return self.type


class CodeBlock(Ast):
    def __init__(self, statements):
        """
            Constructor avoids nesting code blocks 
        """
        if len(statements) == 1 and type(statements[0]) is CodeBlock:
            nestedCodeBlock = statements[0]
            statements = nestedCodeBlock.children
        super().__init__('CodeBlock', children=statements)


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
