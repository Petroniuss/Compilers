from Ast import Ast
from Type import Type
from SymbolTable import SymbolTable


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TypeChecker:

    @addToClass(Ast)
    def typecheck(self, meta, symbolTable: SymbolTable):
        """
            Basic text tree representation.
        """
        pass

    @addToClass(BinaryExpression)
    def typecheck(self, meta, symbolTable: SymbolTable):
        pass
