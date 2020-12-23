import llvmlite.ir as ir
import llvmlite.binding as llvm

intType = ir.IntType(32)
charType = ir.IntType(8)
doubleType = ir.DoubleType()
voidType = ir.VoidType()

intPointerType = intType.as_pointer()
charPointerType = charType.as_pointer()
doublePointerType = doubleType.as_pointer()


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


def isDouble(arg):
    return type(arg.type) == ir.DoubleType


def isInt(arg):
    return type(arg.type) == ir.IntType


def isString(arg):
    pass
    return False


def isVector(arg):
    # here fun begins
    return False


def stringLiteral(literal):
    return ir.Constant.literal_array(
        [ir.Constant(irCharType(), c) for c in literal])


def namedGlobalStringLiteral(module, literal, varName):
    literalArray = stringLiteral(literal)
    glo = ir.GlobalVariable(
        module, literalArray.type, varName)
    glo.global_constant = True
    glo.initializer = literalArray

    return glo


def globalStringPointer(globl):
    return globl.gep([ir.Constant(irIntType(), 0),
                      ir.Constant(irIntType(), 0)])
