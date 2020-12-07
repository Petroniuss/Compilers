from Ast import Ast


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TypeChecker:
    separator = ' | '

    @addToClass(Ast)
    def printTree(self, indent=0):
        """
            Basic text tree representation.
        """
        print(TypeChecker.separator * indent + str(self))
        for child in self.children:
            child.printTree(indent + 1)
