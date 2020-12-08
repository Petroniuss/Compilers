from Ast import *
from Type import *
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
        self.meta = {'errors': []}
        self.ast = ast

    def typecheck(self):
        return self.ast.typecheck(self.meta, self.symbolTable)


def logError(meta: dict, lineno, msg):
    meta['errors'].append((lineno, 'Wrong assignment!'))


@add_method(Ast)
def typecheck(self: Ast, meta: dict, symbolTable: SymbolTable):
    """
        Basic text tree representation.
    """
    for child in self.children:
        child.typecheck(meta, symbolTable)

    return unitType


@add_method(CodeBlock)
def typecheck(self: CodeBlock, meta: dict, symbolTable: SymbolTable):
    symbolTable.pushScope()

    for stmt in self.children:
        stmt.typecheck(meta, symbolTable)

    symbolTable.popScope()

    return unitType


@add_method(Bind)
def typecheck(self: Bind, meta: dict, symbolTable: SymbolTable):
    op = self.operator()
    name = self.name()
    expr = self.expression()

    if symbolTable.contains(name):
        nameType = symbolTable.get(name)
        exprType = expr.typecheck(meta, symbolTable)

    else:
        if op != '=':
            logError(meta, self.lineno, 'Wrong assignment!')
        else:
            exprType = expr.typecheck(meta, symbolTable)
            symbolTable.put(name, exprType)

    return unitType
