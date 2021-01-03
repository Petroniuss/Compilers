import llvmlite.ir as ir
import llvmlite.binding as llvm

intType = ir.IntType(32)
charType = ir.IntType(8)
doubleType = ir.DoubleType()
voidType = ir.VoidType()
nVectorStructType = ir.LiteralStructType([])

intPointerType = intType.as_pointer()
charPointerType = charType.as_pointer()
doublePointerType = doubleType.as_pointer()
nVectorStructPointerType = nVectorStructType.as_pointer()


def irIntPointerType():
    return intPointerType


def irCharPointerType():
    return charPointerType


def irDoublePointerType():
    return doublePointerType


def irVoidType():
    return voidType


def irIntType():
    return intType


def irDoubleType():
    return doubleType


def irCharType():
    return charType


def irNVectorType():
    # this one should not be used! we're operating only on pointers here!
    return nVectorStructType


def irNVectorPointerType():
    return nVectorStructPointerType


def isDouble(arg):
    return arg.type == irDoubleType()


def isInt(arg):
    return arg.type == irIntType()


def isString(arg):
    return arg.type == irCharPointerType()


def isVector(arg):
    return arg.type == irNVectorPointerType()


def doubleArrayInitializer(count):
    return ir.Constant.literal_array(
        [ir.Constant(irDoubleType(), 0.0) for _ in range(count)])


def intArrayInitializer(count):
    return ir.Constant.literal_array(
        [ir.Constant(irIntType(), 0) for _ in range(count)])


def intArrayLiteral(literal):
    return ir.Constant.literal_array(
        [ir.Constant(irIntType(), int(c)) for c in literal])


def stringLiteral(literal):
    return ir.Constant.literal_array(
        [ir.Constant(irCharType(), ord(c)) for c in literal])


def intLiteral(value):
    return ir.Constant(irIntType(), int(value))


def doubleLiteral(value):
    return ir.Constant(irDoubleType(), float(value))


def namedGlobalStringLiteral(module, literal, varName):
    literalArray = stringLiteral(literal)
    glo = ir.GlobalVariable(
        module, literalArray.type, varName)
    glo.global_constant = True
    glo.initializer = literalArray

    return glo


def namedIntArrayLiteral(module, literal, varName):
    literalArray = intArrayLiteral(literal)
    glo = ir.GlobalVariable(
        module, literalArray.type, varName)
    glo.global_constant = True
    glo.initializer = literalArray

    return glo


def arrayPtr(array):
    return array.gep([ir.Constant(irIntType(), 0),
                      ir.Constant(irIntType(), 0)])


def gepArray(array, index):
    return array.gep([ir.Constant(irIntType(), 0),
                      ir.Constant(irIntType(), int(index))])


def gepArrayBuilder(builder, array, index):
    return builder.gep(array, [ir.Constant(irIntType(), 0),
                               ir.Constant(irIntType(), int(index))])


def intArrType(size):
    return ir.ArrayType(irIntType(), size)
