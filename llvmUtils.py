import llvmlite.ir as ir
import llvmlite.binding as llvm

intType = ir.IntType(32)
charType = ir.IntType(8)
doubleType = ir.DoubleType()
voidType = ir.VoidType()


# def getValue(foo):
# foo is either a pointer or literal
# if foo.type == irDoubleType


def irVoidType():
    return voidType


def irIntType():
    return intType


def irDoubleType():
    return doubleType


def irCharType():
    return charType


def isDouble(arg):
    if type(arg) == str:
        return arg == 'double'

    return type(arg.type) == irDoubleType
