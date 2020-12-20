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
        self.builder = ir.IRBuilder()

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


@addMethod(BinaryOp)
def codegen(self: BinaryOp, generator: LLVMCodeGenerator):
    op = self.operator()

    left = self.left().codegen(generator)
    right = self.right().codegen(generator)

    if op == '+':
        return generator.builder.fadd(left, right, 'addTmp')
    elif op == '-':
        return generator.builder.fsub(left, right, 'addTmp')
    elif op == '*':
        return generator.builder.fsub(left, right, 'multTmp')
    elif op == '/':
        return generator.builder.fdiv(left, right, 'divTmp')


@addMethod(Primitive)
def codegen(self: Primitive, generator: LLVMCodeGenerator):
    if self.type == floatType:
        return ir.Constant(ir.DoubleType(), float(self.value()))
    elif self.type == intType:
        # Just to make things simple!
        return ir.Constant(ir.IntType(32), float(self.value()))
    else:
        generator.logError(
            'Only intType and floatType are supported for primitive types!', self.lineno)


@addMethod(CodeBlock)
def codegen(self: CodeBlock, generator: LLVMCodeGenerator):
    anonymousFunction = Function.anonymous(self.children)
    return anonymousFunction.codegen(generator)


@addMethod(Prototype)
def codegen(self: Prototype, generator: LLVMCodeGenerator):
    # FIXME -> This function only handles anonymous functions! aka those from codeblocks!
    functionName = self.name
    functionType = ir.FunctionType(ir.VoidType(), self.args, False)
    irFunction = ir.Function(generator.module, functionType, functionName)

    return irFunction


@addMethod(Function)
def codegen(self: Function, generator: LLVMCodeGenerator):
    # FIXME scoping comes into play! There should be a symbol table somewhere...
    func = self.proto.codegen(generator)
    entryBlock = func.append_basic_block('entry')
    generator.builder = ir.IRBuilder(entryBlock)

    # generate code
    for node in self.body:
        node.codegen(generator)

    retval = ir.VoidType()
    generator.builder.ret_void()

    return func
