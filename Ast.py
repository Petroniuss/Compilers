from Type import intType, floatType, stringType, unitType


class Ast:
    def __init__(self, type, children=None, lineno=0):
        self.type = type
        self.lineno = lineno
        self.children = children if children is not None else []

    def __str__(self):
        return str(self.type)


class For(Ast):
    def __init__(self, id, range, body, lineno=0):
        super().__init__('For', children=[id, range, body], lineno=lineno)

    def id(self):
        return self.children[0]

    def range(self):
        return self.children[1]

    def body(self):
        return self.children[2]


class While(Ast):
    def __init__(self, condition, block, lineno=0):
        super().__init__('While', children=[condition, block], lineno=lineno)

    def condition(self):
        return self.children[0]

    def body(self):
        return self.children[1]


class Break(Ast):
    def __init__(self, lineno=0):
        super().__init__('Break', lineno=lineno)


class Continue(Ast):
    def __init__(self, lineno=0):
        super().__init__('Continue', lineno=lineno)


class Return(Ast):
    def __init__(self, expression, lineno=0):
        super().__init__('Return', children=[expression], lineno=lineno)


class FunctionCall(Ast):
    """
        Built-in functions:
            - transpose (matrix transpose)  -> take vector<>
            - negative (numerical negative) -> float, int, vector
            - zeros -> (int...) -> zeros(1, 2, 3)
            - ones  -> (int...) -> ones(1, 2, 3)
        And also objectCalls like:
            - .+
            - .-
            - .*
            - ./
    """

    def __init__(self, functionName, arglist, lineno=0):
        super().__init__('FunctionCall', children=[
            Leaf(functionName)] + arglist, lineno=lineno)

    def args(self):
        return self.children[1:]

    def functionName(self):
        return self.children[0].value()


class Vector(Ast):
    def __init__(self, elements, lineno=0):
        super().__init__('Vector', children=elements, lineno=lineno)


class SlicedVector(Ast):
    def __init__(self, id, ranges, lineno=0):
        super().__init__('VectorSlice', children=[id] + ranges, lineno=lineno)

    def ranges(self):
        return self.children[1:]

    def id(self):
        return self.children[0]


class RelationalExp(Ast):
    def __init__(self, operator, left, right, lineno=0):
        super().__init__(operator, children=[left, right], lineno=lineno)

    def operator(self):
        return self.type

    def left(self):
        return self.children[0]

    def right(self):
        return self.children[1]


class Bind(Ast):
    def __init__(self, id, assignOperator, expression, lineno=0):
        super().__init__(assignOperator, children=[
            id, expression], lineno=lineno)

    def name(self):
        return self.children[0].name()

    def expression(self):
        return self.children[1]

    def operator(self):
        return self.type


class BindWithSlice(Ast):
    def __init__(self, slicedVector, assignOperator, expression, lineno=0):
        super().__init__(assignOperator, children=[
            slicedVector, expression], lineno=lineno)

    def operator(self):
        return self.type

    def slicedVector(self):
        return self.children[0]

    def expression(self):
        return self.children[1]


class Range(Ast):
    """
        For example: 
            '2:5' 
    """

    def __init__(self, begin, end, lineno=0):
        super().__init__('Range', children=[begin, end], lineno=lineno)

    def begin(self):
        return self.children[0]

    def end(self):
        return self.children[1]


class FromStartRange(Ast):
    """
        For example: 
            '5: ' 
    """

    def __init__(self, end, lineno=0):
        super().__init__('FromStartRange', children=[end], lineno=lineno)

    def end(self):
        return self.children[0]


class EndlessRange(Ast):
    """
        For example: 
            ' :5' 
    """

    def __init__(self, begin, lineno=0):
        super().__init__('EndlessRange', children=[begin], lineno=lineno)

    def begin(self):
        return self.children[0]


class SimpleRange(Ast):
    """
        This is a single index.
    """

    def __init__(self, idx, lineno=0):
        super().__init__('SimpleRange', children=[idx], lineno=lineno)

    def idx(self):
        return self.children[0]


class BinaryOp(Ast):
    def __init__(self, operator, left, right, lineno=0):
        super().__init__(operator, children=[left, right], lineno=lineno)

    def operator(self):
        return self.type

    def left(self):
        return self.children[0]

    def right(self):
        return self.children[1]


class If(Ast):
    def __init__(self, condition, trueBlock, lineno=0):
        super().__init__('If', children=[condition, trueBlock], lineno=lineno)

    def condition(self):
        return self.children[0]

    def trueBlock(self):
        return self.children[1]


class IfElse(Ast):
    def __init__(self, condition, trueBlock, falseBlock, lineno=0):
        super().__init__('IfElse', children=[
            condition, trueBlock, falseBlock], lineno=lineno)

    def condition(self):
        return self.children[0]

    def trueBlock(self):
        return self.children[1]

    def falseBlock(self):
        return self.children[2]


class Identifier(Ast):
    def __init__(self, id, lineno=0):
        super().__init__('ID', children=[Leaf(id)], lineno=lineno)

    def name(self):
        return self.children[0].value()


class Primitive(Ast):
    """
        We might wanna create separate class for each primitive but for now this works.
    """

    def __init__(self, type, value, lineno=0):
        super().__init__(type, children=[Leaf(value)], lineno=lineno)

    def value(self):
        return self.children[0].value()


class Leaf(Ast):
    def __init__(self, value, lineno=0):
        super().__init__(value, children=[], lineno=lineno)

    def value(self):
        return self.type

# todo - figure out how to connect codeblock with prototype and function


class CodeBlock(Ast):
    def __init__(self, statements, lineno=0):
        """
            Constructor avoids nesting code blocks 
        """
        if len(statements) == 1 and type(statements[0]) is CodeBlock:
            nestedCodeBlock = statements[0]
            statements = nestedCodeBlock.children
        super().__init__('CodeBlock', children=statements, lineno=lineno)


class Prototype(Ast):
    def __init__(self, name, ret, args):
        super().__init__('Prototype')
        self.name = name
        self.ret = ret
        self.args = args

    def name(self):
        return self.name

    def retType(self):
        return self.ret

    def args(self):
        return self.args


class Function(Ast):
    _anonymous_function_counter = 0

    def __init__(self, proto, body):
        super().__init__('Function')
        self.proto = proto
        self.body = body

    @classmethod
    def anonymous(cls, body):
        cls._anonymous_function_counter += 1
        proto = Prototype(
            f'_anon_{cls._anonymous_function_counter}', unitType, [])
        return cls(proto, body)

    def isAnonymous(self):
        return self.proto.name().startswith('_anon_')


def String(value, lineno=0):
    return Primitive(stringType, value, lineno=lineno)


def Int(value, lineno=0):
    return Primitive(intType, value, lineno=lineno)


def Float(value, lineno=0):
    return Primitive(floatType, value, lineno=lineno)


def emptyVector():
    return Vector([])
