import llvmlite.ir as ir
import llvmlite.binding as llvm

from decorators import addMethod
from Failure import CodegenError, CompilationFailure
from Ast import *
from Type import *


class LLVMCodeGenerator:
    def __init__(self, ast: Ast):
        self.module = ir.Module()
        self.builder = None
        self.errors = []
        self.astRoot = ast

    def generateIR(self):
        self.astRoot.codegen(self)

        if len(self.errors) > 0:
            raise CompilationFailure('Code generation stage', self.errors)

        pass

    def logError(self, msg, lineno):
        error = CodegenError(msg, lineno)
        self.errors.append(error)


@addMethod(Ast)
def codegen(self: Ast, generator: LLVMCodeGenerator):
    for child in self.children:
        child.codegen(generator)

    return None


@addMethod(Primitive)
def codegen(self: Primitive, generator: LLVMCodeGenerator):
    if self.type == floatType:
        return ir.Constant(ir.DoubleType(), float(self.value()))
    elif self.type == intType:
        return ir.Constant(ir.IntType(32), int(self.value()))
    else:
        generator.logError(
            'Only intType and floatType are supported for primitive types!', self.lineno)
