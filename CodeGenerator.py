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
        ('dotAdd', ir.FunctionType(
            irNVectorPointerType(), [irNVectorPointerType(), irNVectorPointerType()], False)),
        ('dotMinus', ir.FunctionType(
            irNVectorPointerType(), [irNVectorPointerType(), irNVectorPointerType()], False)),
        ('dotMult', ir.FunctionType(
            irNVectorPointerType(), [irNVectorPointerType(), irNVectorPointerType()], False)),
        ('dotDiv', ir.FunctionType(
            irNVectorPointerType(), [irNVectorPointerType(), irNVectorPointerType()], False)),
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
        raise CompilationFailure('Code generation stage', [error])

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
            elif isVector(expr):
                alloca = generator.builder.alloca(
                    irNVectorPointerType(), name=name)
            else:
                generator.raiseError(
                    f'Expected something different! {expr}', self.lineno)

        else:
            alloca = generator.symbolTable.get(name)

        generator.builder.store(expr, alloca)
        generator.symbolTable.put(name, alloca)
    else:
        generator.raiseError(f'Only = operator is supported!', self.lineno)


@addMethod(If)
def codegen(self: If, generator: LLVMCodeGenerator):
    builder = generator.builder
    cmp = self.condition().codegen(generator)

    trueBlock = builder.function.append_basic_block('true-block')
    falseBlock = ir.Block(builder.function, 'false-block')
    mergedBlock = ir.Block(builder.function, 'merged')

    builder.cbranch(cmp, trueBlock, falseBlock)

    # true block
    builder.position_at_start(trueBlock)
    self.trueBlock().codegen(generator)
    builder.branch(mergedBlock)
    trueBlock = generator.builder.block

    # false block (which just branches to merged section)
    builder.function.basic_blocks.append(falseBlock)
    builder.position_at_start(falseBlock)
    builder.branch(mergedBlock)
    falseBlock = generator.builder.block

    builder.function.basic_blocks.append(mergedBlock)
    builder.position_at_start(mergedBlock)

    return mergedBlock


@addMethod(IfElse)
def codegen(self: IfElse, generator: LLVMCodeGenerator):
    builder = generator.builder
    cmp = self.condition().codegen(generator)

    trueBlock = builder.function.append_basic_block('true-block')
    falseBlock = ir.Block(builder.function, 'false-block')
    mergedBlock = ir.Block(builder.function, 'merged')

    builder.cbranch(cmp, trueBlock, falseBlock)

    # true block
    builder.position_at_start(trueBlock)
    self.trueBlock().codegen(generator)
    builder.branch(mergedBlock)
    trueBlock = generator.builder.block

    # false block
    builder.function.basic_blocks.append(falseBlock)
    builder.position_at_start(falseBlock)
    self.falseBlock().codegen(generator)
    builder.branch(mergedBlock)
    falseBlock = generator.builder.block

    builder.function.basic_blocks.append(mergedBlock)
    builder.position_at_start(mergedBlock)

    return mergedBlock


@addMethod(While)
def codegen(self: While, generator: LLVMCodeGenerator):
    builder = generator.builder

    conditionBlock = builder.function.append_basic_block(
        'while-condition-block')
    bodyBlock = ir.Block(builder.function, 'while-body-block')
    mergedBlock = ir.Block(builder.function, 'while-merged')

    builder.branch(conditionBlock)

    # condition block
    builder.position_at_start(conditionBlock)
    cmp = self.condition().codegen(generator)
    builder.cbranch(cmp, bodyBlock, mergedBlock)
    conditionBlock = generator.builder.block

    # body block
    builder.function.basic_blocks.append(bodyBlock)
    builder.position_at_start(bodyBlock)
    self.body().codegen(generator)
    builder.branch(conditionBlock)
    conditionBlock = generator.builder.block

    # merged section
    builder.function.basic_blocks.append(mergedBlock)
    builder.position_at_start(mergedBlock)

    return mergedBlock


@addMethod(For)
def codegen(self: For, generator: LLVMCodeGenerator):
    builder = generator.builder

    initBlock = builder.function.append_basic_block(
        'for-init-block')
    conditionBlock = ir.Block(builder.function, 'for-condition')
    bodyBlock = ir.Block(builder.function, 'for-body-block')
    mergedBlock = ir.Block(builder.function, 'for-merged')

    builder.branch(initBlock)

    # init block
    builder.position_at_start(initBlock)
    left, right = self.range().codegen(generator)
    name = self.id().name()
    alloca = builder.alloca(irIntType(), name=name)
    builder.store(left, alloca)
    generator.symbolTable.put(name, alloca)
    builder.branch(conditionBlock)
    initBlock = generator.builder.block

    # condition block
    builder.function.basic_blocks.append(conditionBlock)
    builder.position_at_start(conditionBlock)
    current = builder.load(alloca)
    current = generator.builder.sitofp(current, irDoubleType())
    limit = generator.builder.sitofp(right, irDoubleType())
    cmp = generator.builder.fcmp_unordered('<=', current, limit, 'for-cmp')
    builder.cbranch(cmp, bodyBlock, mergedBlock)
    conditionBlock = generator.builder.block

    # body block
    builder.function.basic_blocks.append(bodyBlock)
    builder.position_at_start(bodyBlock)
    self.body().codegen(generator)
    current = builder.load(alloca)
    current = builder.add(current, ir.Constant(irIntType(), 1))
    builder.store(current, alloca)
    builder.branch(conditionBlock)
    conditionBlock = generator.builder.block

    # merged block
    builder.function.basic_blocks.append(mergedBlock)
    builder.position_at_start(mergedBlock)

    return mergedBlock


@addMethod(Range)
def codegen(self: Range, generator: LLVMCodeGenerator):
    left, right = self.begin().codegen(generator), self.end().codegen(generator)
    if isDouble(left):
        left = generator.builder.fptosi(left)
    if isDouble(right):
        right = generator.builder.fptosi(right)

    return left, right


@ addMethod(Identifier)
def codegen(self: Identifier, generator: LLVMCodeGenerator):
    name = self.name()
    if not generator.symbolTable.contains(name):
        generator.raiseError(f'Identifier not defined: {name}!', self.lineno)

    ptr = generator.symbolTable.get(name)
    return generator.builder.load(ptr)


@ addMethod(BinaryOp)
def codegen(self: BinaryOp, generator: LLVMCodeGenerator):
    """
        Emitting operations based on type of operands..
    """

    op = self.operator()

    left = self.left().codegen(generator)
    right = self.right().codegen(generator)

    if isVector(left) and isVector(right):
        fname = None
        if op == '+':
            fname = 'dotAdd'
        elif op == '-':
            fname = 'dotMinus'
        elif op == '*':
            fname = 'dotMult'
        elif op == '/':
            fname = 'dotDiv'

        fn = generator.symbolTable.get(fname)
        return generator.builder.call(fn, [left, right])

    if isInt(left) and isInt(right):
        if op == '+':
            return generator.builder.add(left, right, 'addTmp')
        elif op == '-':
            return generator.builder.sub(left, right, 'addTmp')
        elif op == '*':
            return generator.builder.mul(left, right, 'multTmp')
        elif op == '/':
            left = generator.builder.sitofp(left, irDoubleType())
            right = generator.builder.sitofp(right, irDoubleType())

        elif op in ['<', '<=', '>', '>=', '==', '!=']:
            left = generator.builder.sitofp(left, irDoubleType())
            right = generator.builder.sitofp(right, irDoubleType())
            return generator.builder.fcmp_unordered(op, left, right, 'cmp')

    if isInt(left) and isDouble(right):
        left = generator.builder.sitofp(left, irDoubleType())
    elif isDouble(left) and isInt(right):
        right = generator.builder.sitofp(right, irDoubleType())

    if op == '+':
        return generator.builder.fadd(left, right, 'addTmp')
    elif op == '-':
        return generator.builder.fsub(left, right, 'addTmp')
    elif op == '*':
        return generator.builder.fmul(left, right, 'multTmp')
    elif op == '/':
        return generator.builder.fdiv(left, right, 'divTmp')
    elif op in ['<', '<=', '>', '>=', '==', '!=']:
        return generator.builder.fcmp_unordered(op, left, right, 'cmp')


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
    elif name in ['.+', '.-', '.*', './']:
        fn = None
        if name == '.+':
            fn = generator.symbolTable.get('dotAdd')
        elif name == '.-':
            fn = generator.symbolTable.get('dotMinus')
        elif name == '.*':
            fn = generator.symbolTable.get('dotMult')
        elif name == './':
            fn = generator.symbolTable.get('dotDiv')

        args = self.args()
        one, other = args[0].codegen(generator), args[1].codegen(generator)

        return generator.builder.call(fn, [one, other])
    elif name == 'negative':
        arg = self.args()[0].codegen(generator)
        if isInt(arg):
            return generator.builder.neg(arg)
        elif isDouble(arg):
            # This might not work!
            return generator.builder.neg(arg)
    else:
        generator.raiseError(
            f'Other functions are not yet implemented!', self.lineno)


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
