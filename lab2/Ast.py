class Node:
    def __init__(self, type, children=None):
        self.type = type
        self.children = children


class BinaryExpression(Node):
    def __init__(self, operator, leftOperand, rightOperand):
        super().__init__('BinaryExpresion',
                         children=[leftOperand, rightOperand])
        self.operator = operator


class Primitive(Node):
    def __init__(self, type, value):
        super().__init__('Primitive', children=[])
        self.value = value
