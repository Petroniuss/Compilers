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
            irVoidType(), [irCharPointerType()], False)),
        ('zeros', ir.FunctionType(
            irNVectorPointerType(), [irIntType(), irIntPointerType()], False)),
        ('ones', ir.FunctionType(
            irNVectorPointerType(), [irIntType(), irIntPointerType()], False)),
        ('putVectorLn', ir.FunctionType(
            irVoidType(), [irNVectorPointerType()], False)),
        ('literalNVector', ir.FunctionType(
            irNVectorPointerType(), [irIntType(), irIntPointerType(), irDoublePointerType()], False))
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

        # declare extern NVector struct (empty it's defined in runtime library)

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
            else:
                alloca = generator.builder.alloca(
                    irNVectorPointerType(), name=name)
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
    # here we should check types and promote ints to doubles

    if op == '+':
        return generator.builder.fadd(left, right, 'addTmp')
    elif op == '-':
        return generator.builder.fsub(left, right, 'addTmp')
    elif op == '*':
        return generator.builder.fsub(left, right, 'multTmp')
    elif op == '/':
        return generator.builder.fdiv(left, right, 'divTmp')


@ addMethod(Vector)
def codegen(self: Vector, generator: LLVMCodeGenerator):
    # flatten the vector by performing bfs
    q = [self]
    vals = []
    dims = self.dimensions()
    while len(q) > 0:
        popped = q.pop()
        if type(popped) is Vector:
            for child in popped.children:
                q.append(child)
        else:
            vals.append(popped)

    list.reverse(vals)

    valuesArrPtr = doubleArray(vals, generator)
    dimensionsNumber = ir.Constant(irIntType(), int(len(dims)))

    intArry = namedIntArrayLiteral(
        generator.module, dims, generator.nextGlobalName())
    dimensionsPtr = arrayPtr(intArry)

    func = generator.symbolTable.get('literalNVector')
    return generator.builder.call(func, [dimensionsNumber, dimensionsPtr, valuesArrPtr])


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
        return arrayPtr(glob)


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
    if isDouble(arg) or isInt(arg):
        if isDouble(arg):
            formatFunc = generator.symbolTable.get('formatDouble')
        elif isInt(arg):
            formatFunc = generator.symbolTable.get('formatInt')
        arg = generator.builder.call(formatFunc, [arg])

        printFunc = generator.symbolTable.get('putStr')
        generator.builder.call(printFunc, [arg])

        freeStrFunc = generator.symbolTable.get('freeString')
        generator.builder.call(freeStrFunc, [arg])
    elif isString(arg):
        printFunc = generator.symbolTable.get('putStr')
        generator.builder.call(printFunc, [arg])
    elif isVector(arg):
        printFunc = generator.symbolTable.get('putVectorLn')
        generator.builder.call(printFunc, [arg])


@ addMethod(FunctionCall)
def codegen(self: FunctionCall, generator: LLVMCodeGenerator):
    name = self.functionName()
    if name == 'print':
        for arg in self.args():
            handlePrint(arg, generator)
        putLnFunction = generator.symbolTable.get('putLn')
        return generator.builder.call(putLnFunction, [])
    elif name == 'ones' or name == 'zeros':
        n = ir.Constant(irIntType(), len(self.args()))
        ints = intArray(self.args(), generator)

        fn = generator.symbolTable.get(name)
        return generator.builder.call(fn, [n, ints])


#----------------- arrays required by runtime --------------------- #

def intArray(elements, generator: LLVMCodeGenerator):
    builder = generator.builder
    arrType = ir.ArrayType(irIntType(), len(elements))

    glob = ir.GlobalVariable(generator.module, arrType,
                             generator.nextGlobalName())
    glob.initializer = intArrayInitializer(len(elements))

    # calculate index and gep!
    for i, e in enumerate(elements):
        v = e.codegen(generator)
        if isDouble(v):
            v = builder.fptosi(v, irIntType())
        ptr = gepArrayBuilder(builder, glob, i)
        store = builder.store(v, ptr)

    return arrayPtr(glob)


def doubleArray(elements, generator: LLVMCodeGenerator):
    builder = generator.builder
    arrType = ir.ArrayType(irDoubleType(), len(elements))

    glob = ir.GlobalVariable(generator.module, arrType,
                             generator.nextGlobalName())
    glob.initializer = doubleArrayInitializer(len(elements))

    # calculate index and gep!
    for i, e in enumerate(elements):
        v = e.codegen(generator)
        if isInt(v):
            v = builder.sitofp(v, irDoubleType())
        ptr = gepArrayBuilder(builder, glob, i)
        store = builder.store(v, ptr)

    return arrayPtr(glob)
