import llvmlite.ir as ir
import llvmlite.binding as llvm

from llvmUtils import *
from decorators import addMethod
from Failure import CodegenError, CompilationFailure
from SymbolTable import SymbolTable
from Ast import *
from Type import *


class LLVMCodeGenerator:
    standardLibraryFunctions = [
        ('formatInt', ir.FunctionType(
            irCharPointerType(), [irIntType()], False)),
        ('formatDouble', ir.FunctionType(
            irCharPointerType(), [irDoubleType()], False)),
        ('freeString', ir.FunctionType(
            irVoidType(), [irCharPointerType()], False)),
        ('putLn', ir.FunctionType(
            irVoidType(), [], False)),
        ('putStrLn', ir.FunctionType(
            irVoidType(), [irCharPointerType()], False)),
        ('putStr', ir.FunctionType(
            irVoidType(), [irCharPointerType()], False))
    ]

    def __init__(self):
        self.module = ir.Module('Main')
        self.symbolTable = SymbolTable()

        self.builder = ir.IRBuilder()
        self.globalNameGen = self.globalNameGenerator()

    def generateIR(self, ast: Ast):
        # we should also generate declaration for standard library
        for funcName, funcType in LLVMCodeGenerator.standardLibraryFunctions:
            func = ir.Function(self.module, funcType, funcName)
            self.symbolTable.put(funcName, func)

        # start by generating main function
        functionName = 'main'
        functionType = ir.FunctionType(irIntType(), [], False)
        func = ir.Function(self.module, functionType, functionName)
        self.symbolTable.put(functionName, func)

        entryBlock = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entryBlock)

        # traverse ast and generate code
        ast.codegen(self)

        retVal = ir.Constant(irIntType(), 0)
        self.builder.ret(retVal)

        return self.module

    def raiseError(self, msg, lineno):
        error = CodegenError(msg, lineno)
        raise CompilationFailure('Code generation stage', self.errors)

    def nextGlobalName(self):
        return next(self.globalNameGen)

    def globalNameGenerator(self):
        s = 'global_'
        counter = -1
        while True:
            counter += 1
            yield s + str(counter)


@ addMethod(Ast)
def codegen(self: Ast, generator: LLVMCodeGenerator):
    for child in self.children:
        child.codegen(generator)

    return None


@ addMethod(Bind)
def codegen(self: Bind, generator: LLVMCodeGenerator):
    op = self.operator()
    name = self.name()
    expr = self.expression().codegen(generator)

    if op == '=':
        if not generator.symbolTable.contains(name):
            if isDouble(expr):
                alloca = generator.builder.alloca(irDoubleType(), name=name)
            elif isInt(expr):
                alloca = generator.builder.alloca(irIntType(), name=name)
            elif isString(expr):
                alloca = generator.builder.alloca(
                    irCharPointerType(), name=name)

            print(expr, expr.type)
        else:
            alloca = generator.symbolTable.get(name)

        generator.builder.store(expr, alloca)
        generator.symbolTable.put(name, alloca)
    else:
        generator.raiseError(f'Only = operator is supported!', self.lineno)


@ addMethod(Identifier)
def codegen(self: Identifier, generator: LLVMCodeGenerator):
    name = self.name()
    if not generator.symbolTable.contains(name):
        generator.raiseError(f'Identifier not defined: {name}!', self.lineno)

    ptr = generator.symbolTable.get(name)
    return generator.builder.load(ptr)


@ addMethod(BinaryOp)
def codegen(self: BinaryOp, generator: LLVMCodeGenerator):
    op = self.operator()

    left = self.left().codegen(generator)
    right = self.right().codegen(generator)
    # print(left.type, right)
    # here we should check types and promote ints to doubles

    if op == '+':
        return generator.builder.fadd(left, right, 'addTmp')
    elif op == '-':
        return generator.builder.fsub(left, right, 'addTmp')
    elif op == '*':
        return generator.builder.fsub(left, right, 'multTmp')
    elif op == '/':
        return generator.builder.fdiv(left, right, 'divTmp')


@ addMethod(Primitive)
def codegen(self: Primitive, generator: LLVMCodeGenerator):
    # Just to make things simple I only have double type for now!
    if self.type == floatType:
        return ir.Constant(irDoubleType(), float(self.value()))
    elif self.type == intType:
        return ir.Constant(irIntType(), int(self.value()))
    elif self.type == stringType:
        globName = generator.nextGlobalName()
        glob = namedGlobalStringLiteral(
            generator.module, str(self.value() + '\x00'), globName)
        return globalToPtr(glob)
    else:
        generator.raiseError(
            'Vectors not yet supported :/', self.lineno)


@ addMethod(CodeBlock)
def codegen(self: CodeBlock, generator: LLVMCodeGenerator):
    generator.symbolTable.pushScope()
    for node in self.children:
        node.codegen(generator)
    generator.symbolTable.popScope()

    return irVoidType()


# ----------------------- Function Calls -----------------------------

def handlePrint(arg, generator: LLVMCodeGenerator):
    arg = arg.codegen(generator)
    formatFunc = None
    if isDouble(arg):
        formatFunc = generator.symbolTable.get('formatDouble')
    elif isInt(arg):
        formatFunc = generator.symbolTable.get('formatInt')
    elif isVector(arg):
        pass

    if not isString(arg):
        arg = generator.builder.call(formatFunc, [arg])

        printFunc = generator.symbolTable.get('putStr')
        generator.builder.call(printFunc, [arg])

        freeStrFunc = generator.symbolTable.get('freeString')
        generator.builder.call(freeStrFunc, [arg])
    else:
        printFunc = generator.symbolTable.get('putStr')
        generator.builder.call(printFunc, [arg])


@addMethod(FunctionCall)
def codegen(self: FunctionCall, generator: LLVMCodeGenerator):
    name = self.functionName()
    if name == 'print':
        for arg in self.args():
            handlePrint(arg, generator)
        putLnFunction = generator.symbolTable.get('putLn')
        return generator.builder.call(putLnFunction, [])

# --------------------------------------------------------------------


# We don't use this kind of stuff!

# @ addMethod(Prototype)
# def codegen(self: Prototype, generator: LLVMCodeGenerator):
#     # FIXME -> This function only handles anonymous functions! aka those from codeblocks!
#     functionName = self.name
#     functionType = ir.FunctionType(ir.VoidType(), self.args, False)
#     irFunction = ir.Function(generator.module, functionType, functionName)
#     generator.symbolTable.put(functionName, irFunction)

#     return irFunction


# @ addMethod(Function)
# def codegen(self: Function, generator: LLVMCodeGenerator):
#     # FIXME scoping comes into play! There should be a symbol table somewhere...
#     func = self.proto.codegen(generator)
#     entryBlock = func.append_basic_block('entry')
#     generator.builder = ir.IRBuilder(entryBlock)

#     # generate code
#     for node in self.body:
#         node.codegen(generator)

#     retval = ir.VoidType()
#     generator.builder.ret_void()

#     return func
