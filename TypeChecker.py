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

    if symbolTable.contains(name):
        nameType = symbolTable.get(name)
        errors, newType = nameType.unifyBinary('=', exprType)

        logErrors(meta, self.lineno, errors)
        if newType is not None:
            symbolTable.replace(name, newType)

    else:
        if exprType is not None:
            symbolTable.put(name, exprType)
        # else:
            # logErrors(meta, self.lineno, ["Bad assignment!"])

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

    if leftType is None or rightType is None:
        return None

    op = self.operator()
    errors, unified = leftType.unifyBinary(op, rightType)
    logErrors(meta, self.lineno, errors)

    return unified


@add_method(Vector)
def typecheck(self: Vector, meta: dict, symbolTable: SymbolTable):
    if len(self.children) < 1:
        return emptyVectorType

    typesSet = set()
    ttypes = []
    for e in self.children:
        ttype = e.typecheck(meta, symbolTable)
        if ttype is None:
            return None

        typesSet.add(ttype.type())
        ttypes.append(ttype)

    if len(typesSet) > 1:
        errors = [f'Vector contains elements of multiple types: {typesSet}!']
        logErrors(meta, self.lineno, errors)
        return None

    acc = ttypes[0]
    sizes = [len(self.children)]
    innerType = acc
    if type(acc) is VectorType:
        sizes += acc.size
        innerType = acc.eType

    return VectorType(innerType, sizes)


@add_method(RelationalExp)
def typecheck(self: RelationalExp, meta: dict, symbolTable: SymbolTable):
    leftType = self.left().typecheck(meta, symbolTable)
    rightType = self.right().typecheck(meta, symbolTable)

    if leftType is None or rightType is None:
        return None

    op = self.operator()
    errors, unified = leftType.unifyBinary(op, rightType)
    logErrors(meta, self.lineno, errors)

    return unified


@add_method(If)
def typecheck(self: If, meta: dict, symbolTable: SymbolTable):
    self.trueBlock().typecheck(meta, symbolTable)

    conditionType = self.condition().typecheck(meta, symbolTable)
    if conditionType is not None and conditionType != booleanType:
        logErrors(meta, self.lineno, [
                  f'Condition in if statement must be of type boolean, not {conditionType}!'])

    return unitType


@add_method(IfElse)
def typecheck(self: IfElse, meta: dict, symbolTable: SymbolTable):
    self.trueBlock().typecheck(meta, symbolTable)
    self.falseBlock().typecheck(meta, symbolTable)

    conditionType = self.condition().typecheck(meta, symbolTable)
    if conditionType is not None and conditionType != booleanType:
        logErrors(meta, self.lineno, [
                  f'Condition in if-else statement must be of type {booleanType}, not {conditionType}!'])

    return unitType


@add_method(SlicedVector)
def typecheck(self: SlicedVector, meta: dict, symbolTable: SymbolTable):
    """
        Boring, error-prone code. To indicate unknown size I use -1 in the unknown dimension.
    """
    vectorType = self.id().typecheck(meta, symbolTable)
    if vectorType is None:
        return None

    if type(vectorType) is not VectorType:
        logErrors(meta, self.lineno, [
                  f'Slicing types other than vector - {vectorType} is forbidden!'])

        return None

    invalid = False
    errors = []
    newSize = []

    def validateRange(l, r, size):
        nonlocal invalid
        if r > size and r != -1:
            errors.append(
                f'Trying to access elements outside vector - [{l}, {r}) from [0, {size})')
            invalid = True

        newSize.append(r - l)

    ranges = self.ranges()
    sizes = vectorType.size
    for i, r in enumerate(ranges):
        if r.typecheck(meta, symbolTable) is None:
            invalid = True
        elif i >= len(sizes):
            errors.append(
                f'Trying to access {i + 1} dimension in {len(sizes)} dimensional vector!')
        elif type(r) is SimpleRange:
            idx = r.idx()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(index, index + 1, sizes[i])
            else:
                newSize.append(1)

        elif type(r) is FromStartRange:
            idx = r.end()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(0, index, sizes[i])
            else:
                newSize.append(-1)

        elif type(r) is EndlessRange:
            idx = r.begin()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(index, sizes[i], sizes[i])
            else:
                newSize.append(-1)

        elif type(r) is Range:
            l, r = r.begin(), r.end()
            if type(l) is Primitive and type(r) is Primitive:
                l, r = l.value(), r.value()
                validateRange(l, r, sizes[i])
            else:
                newSize.append(-1)

        else:
            raise Exception('How did we get here!?')

    for i in range(len(ranges), len(sizes)):
        newSize.append(sizes[i])

    if invalid is True:
        logErrors(meta, self.lineno, errors)
        return None

    # We pop dimensions
    i = 0
    while i < len(newSize) and newSize[i] == 1:
        i += 1

    newSize = newSize[i:]

    # in case we return single element
    if len(newSize) < 1:
        return vectorType.eType

    return VectorType(vectorType.eType, newSize)


@add_method(SimpleRange)
def typecheck(self: SimpleRange, meta: dict, symbolTable: SymbolTable):
    id = self.idx()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        logErrors(meta, self.lineno, [
                  f'Index can only be of [{intType}] type not [{ttype}] type'])
        return None

    return unitType


@add_method(EndlessRange)
def typecheck(self: EndlessRange, meta: dict, symbolTable: SymbolTable):
    id = self.begin()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        logErrors(meta, self.lineno, [
                  f'Index can only be of [:{intType}] type not [:{ttype}] type'])
        return None

    return unitType


@add_method(FromStartRange)
def typecheck(self: FromStartRange, meta: dict, symbolTable: SymbolTable):
    id = self.end()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        logErrors(meta, self.lineno, [
                  f'Index can only be of [{intType}:] type not [{ttype}:] type'])
        return None

    return unitType


@add_method(Range)
def typecheck(self: Range, meta: dict, symbolTable: SymbolTable):
    begin, end = self.begin(), self.end()
    beginType = begin.typecheck(meta, symbolTable)
    endType = end.typecheck(meta, symbolTable)

    if beginType != intType or endType != intType:
        logErrors(meta, self.lineno, [
                  f'Range can only be of [{intType}:{intType}] type not [{beginType}:{endType}] type'])
        return None

    return unitType


@add_method(BindWithSlice)
def typecheck(self: BindWithSlice, meta: dict, symbolTable: SymbolTable):
    vType = self.slicedVector().typecheck(meta, symbolTable)
    expType = self.expression().typecheck(meta, symbolTable)

    if vType is None or expType is None:
        return None

    oop = self.operator()
    errors, newType = vType.unifyBinary(oop, expType)
    logErrors(meta, self.lineno, errors)

    return unitType


@add_method(FunctionCall)
def typecheck(self: FunctionCall, meta: dict, symbolTable: SymbolTable):
    pass


# functionCallTypeCheckers: {
#     'transpose': foo,
#     'negative': foo,
#     'zeros': foo,
#     'ones': foo,
#     '.+': foo,
#     '.-': foo,
#     '.*': foo,
#     './': foo
# }


def typeCheckTranspose(self: FunctionCall, meta: dict, symbolTable: SymbolTable):
    vectorType = self.args()[0].typecheck(meta, symbolTable)
    if vectorType is None:
        return None

    if type(vectorType) is not VectorType:
        logErrors(meta, self.lineno, [
                  f'Transpose takes matrix not {vectorType}'])
        return None

    size = vectorType.size
    if len(size) != 2:
        logErrors(meta, self.lineno, [f'We can only tranpose matrices!'])
        return None

    newSize = [size[1], size[0]]
    eType = vectorType.eType

    return VectorType(eType, newSize)


def typeCheckNegative(self: FunctionCall, meta: dict, symbolTable: SymbolTable):
    ttype = self.args()[0].typecheck(meta, symbolTable)
    if ttype is None:
        return None

    if not isNumericType(ttype):
        logErrors(meta, self.lineno, [
                  f'We can calculate negative only of numeric types not {ttype}!'])
        return None

    return ttype


def typeCheckNegative(self: FunctionCall, meta: dict, symbolTable: SymbolTable):
    sizes = []
    args = self.args()

    errors = []
    for arg in args:
        argType = arg.typecheck(meta, symbolTable)

        if argType != intType:
            errors.append([f'Invalid argument {argType} instead of {intType}'])
        else:
            if type(arg) is Primitive:
                sizes.append(arg.value())
            else:
                sizes.append(-1)

    if len(errors) > 0:
        logErrors(meta, self.lineno, errors)
        return None

    return Vector(floatType, sizes)
