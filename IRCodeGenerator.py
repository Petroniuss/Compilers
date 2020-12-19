from decorators import addMethod
from Ast import *

import llvmlite


@addMethod(Ast)
def codegen(self: Ast):
    for child in self.children:
        child.typecheck(meta, symbolTable)

    return unitType
