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


class TypeChecker:
    def __init__(self, ast: Ast):
        self.symbolTable = SymbolTable()
        self.meta = {'errors': []}
        self.ast = ast

    def typecheck(self):
        self.ast.typecheck(self.meta, self.symbolTable)

        print(self.meta)


def logErrors(meta: dict, lineno, msgs):
    errors = meta['errors']
    for msg in msgs:
        errors.append((lineno, msg))


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

    exprType = expr.typecheck(meta, symbolTable)
    print('Bind name ' + name)

    if symbolTable.contains(name):
        nameType = symbolTable.get(name)
        errors, newType = nameType.unifyBinary(exprType)

        logErrors(meta, self.lineno, errors)
        if newType is not None:
            symbolTable.replace(name, newType)

    else:
        if exprType is not None:
            symbolTable.put(name, exprType)
        else:
            logErrors(meta, self.lineno, ["Bad assignment!"])

    return unitType


@add_method(Identifier)
def typecheck(self: Identifier, meta: dict, symbolTable: SymbolTable):
    name = self.name()

    if not symbolTable.contains(name):
        logErrors(meta, self.lineno, [f'Identifier not defined: {name}!'])
        return None

    return symbolTable.get(name)


@add_method(Primitive)
def typecheck(self: Primitive, meta: dict, symbolTable: SymbolTable):
    return self.type


@add_method(BinaryOp)
def typecheck(self: BinaryOp, meta: dict, symbolTable: SymbolTable):
    leftType = self.left().typecheck(meta, symbolTable)
    rightType = self.right().typecheck(meta, symbolTable)

    op = self.operator()

    errors, unified = leftType.unifyBinary(op, rightType)
    print(errors, unified)
    logErrors(meta, self.lineno, errors)

    return unified
