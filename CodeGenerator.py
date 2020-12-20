import llvmlite.ir as ir
import llvmlite.binding as llvm

from decorators import addMethod
from Failure import CodegenError, CompilationFailure
from Ast import *
from Type import *


class LLVMCodeGenerator:
    def __init__(self):
        self.module = ir.Module('Main')
        self.errors = []

        # This thing should be accessible within some scope!
        self.builder = None

    def generateIR(self, ast: Ast):
        ast.codegen(self)

        if len(self.errors) > 0:
            raise CompilationFailure('Code generation stage', self.errors)

        return self.module

    def logError(self, msg, lineno):
        error = CodegenError(msg, lineno)
        self.errors.append(error)


@addMethod(Ast)
def codegen(self: Ast, generator: LLVMCodeGenerator):
    for child in self.children:
        child.codegen(generator)

    return None


@addMethod(CodeBlock)
def codegen(self: CodeBlock, generator: LLVMCodeGenerator):
    # Figure out how to emit phi!
    pass


@addMethod(BinaryOp)
def codegen(self: BinaryOp, generator: LLVMCodeGenerator):
    op = self.operator()

    left = self.left().codegen(generator)
    right = self.right().codegen(generator)

    if op == '+':
        pass
    elif op == '-':
        pass
    elif op == '*':
        pass
    elif op == '/':
        pass

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
