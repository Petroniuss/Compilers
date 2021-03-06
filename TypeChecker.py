from Ast import *
from Type import *
from SymbolTable import SymbolTable
from Failure import TypeError, CompilationFailure
from decorators import addMethod


class TypeChecker:
    def __init__(self, ast: Ast):
        self.symbolTable = SymbolTable()
        self.meta = {
            'errors': [],
            'loop': 0
        }
        self.ast = ast

    def typecheck(self):
        self.ast.typecheck(self.meta, self.symbolTable)
        errors = self.meta['errors']

        if len(errors) >= 1:
            errors = map(lambda tpl: TypeError(
                tpl[1], tpl[0]), errors)

            raise CompilationFailure('Type checking failed', list(errors))


def gatherErrors(meta: dict, lineno, msgs):
    errors = meta['errors']
    for msg in msgs:
        errors.append((lineno, msg))


@addMethod(Ast)
def typecheck(self: Ast, meta: dict, symbolTable: SymbolTable):
    for child in self.children:
        child.typecheck(meta, symbolTable)

    return unitType


@addMethod(CodeBlock)
def typecheck(self: CodeBlock, meta: dict, symbolTable: SymbolTable):
    symbolTable.pushScope()

    for stmt in self.children:
        stmt.typecheck(meta, symbolTable)

    symbolTable.popScope()

    return unitType


@addMethod(Bind)
def typecheck(self: Bind, meta: dict, symbolTable: SymbolTable):
    name = self.name()
    expr = self.expression()

    exprType = expr.typecheck(meta, symbolTable)
    if exprType is None:
        return None

    if symbolTable.contains(name):
        nameType = symbolTable.get(name)
        errors, newType = nameType.unifyBinary('=', exprType)

        gatherErrors(meta, self.lineno, errors)
        if newType is not None:
            symbolTable.replace(name, newType)
    else:
        symbolTable.put(name, exprType)

    return unitType


@addMethod(Identifier)
def typecheck(self: Identifier, meta: dict, symbolTable: SymbolTable):
    name = self.name()

    if not symbolTable.contains(name):
        gatherErrors(meta, self.lineno, [f'Identifier not defined: {name}!'])
        return None

    return symbolTable.get(name)


@addMethod(Primitive)
def typecheck(self: Primitive, meta: dict, symbolTable: SymbolTable):
    return self.type


@addMethod(BinaryOp)
def typecheck(self: BinaryOp, meta: dict, symbolTable: SymbolTable):
    leftType = self.left().typecheck(meta, symbolTable)
    rightType = self.right().typecheck(meta, symbolTable)

    if leftType is None or rightType is None:
        return None

    op = self.operator()
    errors, unified = leftType.unifyBinary(op, rightType)
    gatherErrors(meta, self.lineno, errors)

    return unified


@addMethod(Vector)
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
        gatherErrors(meta, self.lineno, errors)
        return None

    acc = ttypes[0]
    sizes = [len(self.children)]
    innerType = acc
    # To handle multidimensional vectors
    if type(acc) is VectorType:
        sizes += acc.shape
        innerType = acc.innerType

    if not (innerType == intType or innerType == floatType):
        errors = [f'We only have numeric vectors not {innerType}!']
        gatherErrors(meta, self.lineno, errors)
        return None

    return VectorType(innerType, sizes)


# @addMethod(RelationalExp)
# def typecheck(self: RelationalExp, meta: dict, symbolTable: SymbolTable):
#     leftType = self.left().typecheck(meta, symbolTable)
#     rightType = self.right().typecheck(meta, symbolTable)

#     if leftType is None or rightType is None:
#         return None

#     ops = self.operator()
#     errors, unified = leftType.unifyBinary(ops, rightType)
#     gatherErrors(meta, self.lineno, errors)

#     return unified


@addMethod(If)
def typecheck(self: If, meta: dict, symbolTable: SymbolTable):
    self.trueBlock().typecheck(meta, symbolTable)

    conditionType = self.condition().typecheck(meta, symbolTable)
    if conditionType is not None and conditionType != booleanType:
        gatherErrors(meta, self.lineno, [
            f'Condition in if statement must be of type boolean, not {conditionType}!'])

    return unitType


@addMethod(IfElse)
def typecheck(self: IfElse, meta: dict, symbolTable: SymbolTable):
    self.trueBlock().typecheck(meta, symbolTable)
    self.falseBlock().typecheck(meta, symbolTable)

    conditionType = self.condition().typecheck(meta, symbolTable)
    if conditionType is not None and conditionType != booleanType:
        gatherErrors(meta, self.lineno, [
            f'Condition in if-else statement must be of type {booleanType}, not {conditionType}!'])

    return unitType


@addMethod(SlicedVector)
def typecheck(self: SlicedVector, meta: dict, symbolTable: SymbolTable):
    """
            Behold! Black magic ahead..>
    """
    vectorType = self.id().typecheck(meta, symbolTable)
    if vectorType is None:
        return None

    if type(vectorType) is not VectorType:
        gatherErrors(meta, self.lineno, [
            f'Slicing types other than vector - {vectorType} is forbidden!'])

        return None

    if vectorType.dimensions() < len(self.ranges()):
        gatherErrors(meta, self.lineno, [
            f'Slice has more dimensions than this vector has {vectorType.dimensions()} and {len(self.ranges())}'])

        return None

    invalid = False
    errors = []
    newShape = []

    def validateRange(l, r, size):
        nonlocal invalid
        if r > size and r != -1:
            errors.append(
                f'Trying to access elements outside vector - [{l}, {r}) from [0, {size})')
            invalid = True

        newShape.append(r - l)

    ranges = self.ranges()
    shape = vectorType.shape
    for i, r in enumerate(ranges):
        if r.typecheck(meta, symbolTable) is None:
            invalid = True
        elif i >= len(shape):
            errors.append(
                f'Trying to access {i + 1} dimension in {len(shape)} dimensional vector!')
        elif type(r) is SimpleRange:
            idx = r.idx()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(index, index + 1, shape[i])
            else:
                newShape.append(1)

        elif type(r) is FromStartRange:
            idx = r.end()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(0, index, shape[i])
            else:
                newShape.append(-1)

        elif type(r) is EndlessRange:
            idx = r.begin()
            if type(idx) is Primitive:
                index = idx.value()
                validateRange(index, shape[i], shape[i])
            else:
                newShape.append(-1)

        elif type(r) is Range:
            l, r = r.begin(), r.end()
            if type(l) is Primitive and type(r) is Primitive:
                l, r = l.value(), r.value()
                validateRange(l, r, shape[i])
            else:
                newShape.append(-1)

        else:
            raise Exception('How did we get here!?')

    for i in range(len(ranges), len(shape)):
        newShape.append(shape[i])

    if invalid is True:
        gatherErrors(meta, self.lineno, errors)
        return None

    # We pop dimensions
    i = 0
    while i < len(newShape) and newShape[i] == 1:
        i += 1

    newShape = newShape[i:]

    # in case we return single element
    if len(newShape) < 1:
        return vectorType.innerType

    return VectorType(vectorType.innerType, newShape)


@addMethod(SimpleRange)
def typecheck(self: SimpleRange, meta: dict, symbolTable: SymbolTable):
    id = self.idx()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        gatherErrors(meta, self.lineno, [
            f'Index can only be of [{intType}] type not [{ttype}] type'])
        return None

    return unitType


@addMethod(EndlessRange)
def typecheck(self: EndlessRange, meta: dict, symbolTable: SymbolTable):
    id = self.begin()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        gatherErrors(meta, self.lineno, [
            f'Index can only be of [:{intType}] type not [:{ttype}] type'])
        return None

    return unitType


@addMethod(FromStartRange)
def typecheck(self: FromStartRange, meta: dict, symbolTable: SymbolTable):
    id = self.end()
    ttype = id.typecheck(meta, symbolTable)

    if ttype != intType:
        gatherErrors(meta, self.lineno, [
            f'Index can only be of [{intType}:] type not [{ttype}:] type'])
        return None

    return unitType


@addMethod(Range)
def typecheck(self: Range, meta: dict, symbolTable: SymbolTable):
    begin, end = self.begin(), self.end()
    beginType = begin.typecheck(meta, symbolTable)
    endType = end.typecheck(meta, symbolTable)

    if beginType is None or endType is None:
        return None

    if beginType != intType or endType != intType:
        gatherErrors(meta, self.lineno, [
            f'Range can only be of [{intType}:{intType}] type not [{beginType}:{endType}] type'])
        return None

    return unitType


@addMethod(BindWithSlice)
def typecheck(self: BindWithSlice, meta: dict, symbolTable: SymbolTable):
    vType = self.slicedVector().typecheck(meta, symbolTable)
    expType = self.expression().typecheck(meta, symbolTable)

    if vType is None or expType is None:
        return None

    ops = self.operator()
    errors, newType = vType.unifyBinary(ops, expType)
    gatherErrors(meta, self.lineno, errors)

    return unitType


@addMethod(Return)
def typecheck(self: Return, meta: dict, symbolTable: SymbolTable):
    if meta.get('loop', 0) == 0:
        gatherErrors(meta, self.lineno, [
                     f'Return keyword not allowed since there\'re no user defined functions!'])

    return unitType


@addMethod(Continue)
def typecheck(self: Continue, meta: dict, symbolTable: SymbolTable):
    if meta.get('loop', 0) == 0:
        gatherErrors(meta, self.lineno, [
                     f'Continue keyword only allowed within a loop!'])

    return unitType


@addMethod(Break)
def typecheck(self: Break, meta: dict, symbolTable: SymbolTable):
    if meta.get('loop', 0) == 0:
        gatherErrors(meta, self.lineno, [
                     f'Break keyword only allowed within a loop!'])

    return unitType


@addMethod(While)
def typecheck(self: While, meta: dict, symbolTable: SymbolTable):
    conditionType = self.condition().typecheck(meta, symbolTable)

    if conditionType is not None and conditionType != booleanType:
        gatherErrors(meta, self.lineno, [
            f'Condition in while statement must be of type boolean, not {conditionType}!'])

    meta['loop'] += 1
    self.body().typecheck(meta, symbolTable)
    meta['loop'] -= 1

    return unitType


@addMethod(For)
def typecheck(self: For, meta: dict, symbolTable: SymbolTable):
    self.range().typecheck(meta, symbolTable)

    name = self.id().name()
    symbolTable.put(name, intType)

    meta['loop'] += 1
    self.body().typecheck(meta, symbolTable)
    meta['loop'] -= 1

    return unitType

# -------------------------------------------------
# ---- Typechecking built-in functions ------------
# -------------------------------------------------


def typecheckUnaryTwoDimensionalVector(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        Vector<Any>[x, y] -> Vector<Any>[y, x]
    """
    if len(args) < 1:
        return [f'Function {fname} takes one argument, zero given'], None

    vectorType = args[0].typecheck(meta, symbolTable)
    if vectorType is None:
        return [], None

    if type(vectorType) is not VectorType:
        return [f'Function {fname} takes matrix not {vectorType}'], None

    if vectorType.dimensions() != 2:
        return [f'We can only tranpose 2-dimensional vectors aka matrices!'], None

    shape = vectorType.shape
    newShape = [shape[1], shape[0]]
    innerType = vectorType.innerType

    return [], VectorType(innerType, newShape)


def typeCheckUnaryNumieric(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        Numeric -> Numeric 
    """
    if len(args) != 1:
        return [f'Function {fname} takes exactly one argument'], None

    ttype = args[0].typecheck(meta, symbolTable)
    if ttype is None:
        return [], None

    if not isNumericType(ttype):
        return [f'Function {fname} takes numeric type not {ttype}!'], None

    return [], ttype


def typeCheckIntVarargsToVector(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        [Int...] -> Vector
    """
    if len(args) < 1:
        return [f'Function {fname} takes at least one argument!'], None

    invalid = False
    newShape = []
    argTypes = []
    for arg in args:
        argType = arg.typecheck(meta, symbolTable)

        if argType != intType:
            invalid = True
        else:
            if type(arg) is Primitive:
                newShape.append(arg.value())
            else:
                newShape.append(-1)

        argTypes.append(argType)

    if invalid:
        correct = [intType] * len(args)
        return [f'Invalid arguments to function {fname}: expected {correct}, got {argTypes}'], None

    return [], VectorType(floatType, newShape)


def typecheckVectorDotCall(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        [Vector, Vector] -> Vector
    """
    if len(args) != 2:
        return [f'Function {fname} takes two arguments not {len(args)}!']

    v1, v2 = args
    v1Type, v2Type = v1.typecheck(
        meta, symbolTable), v2.typecheck(meta, symbolTable)

    if v1Type is None or v2Type is None:
        return [], None

    return v1Type.unifyBinary(fname, v2Type)


def typecheckEye(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        Int -> Vector<Float>[Int, Int] 
    """
    if len(args) < 1:
        return [f'Function {fname} takes one argument, zero given'], None

    arg = args[0]
    argType = arg.typecheck(meta, symbolTable)

    if argType is None:
        return [], None

    if argType != intType:
        return [f'Function {fname} takes {intType} not {argType}'], None

    newShape = [-1, -1]
    if type(arg) is Primitive:
        newShape = [arg.value(), arg.value()]

    innerType = floatType

    return [], VectorType(innerType, newShape)


def typecheckPrint(fname: str, args: list, meta: dict, symbolTable: SymbolTable):
    """
        [Any...] -> Vector
    """
    if len(args) < 1:
        return [f'Function {fname} takes at least one argument!']

    for arg in args:
        arg.typecheck(meta, symbolTable)

    return [], unitType


functionCallTypeCheckDispatcher = {
    'transpose': typecheckUnaryTwoDimensionalVector,
    'negative': typeCheckUnaryNumieric,
    'zeros': typeCheckIntVarargsToVector,
    'ones': typeCheckIntVarargsToVector,
    'eye': typecheckEye,
    'print': typecheckPrint,
    '.+': typecheckVectorDotCall,
    '.-': typecheckVectorDotCall,
    '.*': typecheckVectorDotCall,
    './': typecheckVectorDotCall
}


@addMethod(FunctionCall)
def typecheck(self: FunctionCall, meta: dict, symbolTable: SymbolTable):
    name = self.functionName()
    args = self.args()

    typecheckFun = functionCallTypeCheckDispatcher[name]

    errors, ttype = typecheckFun(name, args, meta, symbolTable)
    gatherErrors(meta, self.lineno, errors)

    return ttype
