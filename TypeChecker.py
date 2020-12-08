from Ast import *
from Type import Type
from SymbolTable import SymbolTable

from functools import wraps


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        return wrapper

    return decorator


typeTable = {
    'BinaryExpression': 1,
    'RelationalExpr': 2
}


class TypeChecker:
    def __init__(self, ast: Ast):
        self.symbolTable = SymbolTable()
        self.meta = {}
        self.ast = ast

    def typecheck(self):
        return self.ast.typecheck(self.meta, self.symbolTable)


@add_method(Ast)
def typecheck(self: Ast, meta: dict, symbolTable: SymbolTable):
    """
        Basic text tree representation.
    """
    for child in self.children:
        symbolTable.pushScope()
        child.typecheck(meta, symbolTable)
        symbolTable.popScope()


@add_method(CodeBlock)
def typecheck(self: CodeBlock, meta: dict, symbolTable: SymbolTable):
    for stmt in self.children:
        stmt.typecheck(meta, symbolTable)


@add_method(Bind)
def typecheck(self: Bind, meta: dict, symbolTable: SymbolTable):
    op = self.operator()

    # init bind
    if op == '=':
        name = self.name()
    # update bind
    else:
        pass
