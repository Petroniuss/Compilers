from typing import List
from enum import Enum

# ----------------------------------------------
# --------    Type definitions       -----------
# ----------------------------------------------


class Type:
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.type()

    def type(self):
        return 'Unit'

    def unifyBinary(self, ops, other: 'Type') -> ([str], 'Type'):
        """
            When performing binary operation either we get list of errors or new type.
        """
        if type(self) != type(other):
            return ([f"Cannot unify these two types {self} and {other}!"], None)

        return self._unifyBinary(ops, other)

    def _unifyBinary(self, ops: str, other: 'Type'):
        return ([], self)


class PrimitiveType(Type):
    """
        Primitive type like 'Int'
    """

    def __init__(self, tname: str):
        self.tname = tname

    def type(self):
        return self.tname

    def _unifyBinary(self, ops: str, other: 'Primitive'):
        t1, t2 = self, other
        if ops in binaryOpsTypeTable:
            table = binaryOpsTypeTable[ops]
            if t1 in table:
                table = table[t1]
                if t2 in table:
                    return ([], table[t2])

        return ([f'Cannot unify types {t1} and {t2} via {ops} operation!'], None)


class VectorType(Type):
    """
        Multidimensional vector like 'Vector<Float>[2, 3, 5]'

        Shape contains sizes along each dimensio of our vector.

        Note to indicate that we don't know size along particular dimension we put -1 in that row.
        For example 'Vector<int>[2, -1, -1]'
    """

    def __init__(self, eType: PrimitiveType, size: List[int]):
        self.innerType = eType
        self.shape = size

    def type(self):
        return f'Vector<{self.innerType.type()}>{self.shape}'

    def dimensions(self):
        return len(self.shape)

    def dimensionsMatch(self, other: 'VectorType'):
        if self.dimensions() != other.dimensions():
            return [f'Vector have different number of dimensions: {self.dimensions()} and {other.dimensions}']

        return []

    def newShape(self, other: 'VectorType'):
        newShape = []
        for s1, s2 in zip(self.shape, other.shape):
            if s1 != s2 and (s1 != -1 or s2 != -1):
                return [f'Shapes don\'t match: {self.shape} and {other.shape}!'], []

            if s1 == -1 or s2 == -1:
                newShape.append(-1)
            else:
                newShape.append(s1)

        return [], newShape

    def _unifyBinary(self, ops: str, other: 'VectorType'):
        errors, newPrimitiveType = self.innerType.unifyBinary(
            ops, other.innerType)

        dimensionErrors = self.dimensionsMatch(other)
        shapeErrors, newShape = self.newShape(other)

        errors += dimensionErrors
        errors += shapeErrors

        newType = VectorType(newPrimitiveType, newShape) if len(
            errors) < 1 else None

        return errors, newType


def isNumericType(type: Type):
    if type(type) is PrimitiveType:
        return type == intType or type == floatType

    elif type(type) is VectorType:
        return isNumericType(type.innerType)

    return False


class AnyType(Type):
    def type(self):
        return 'Any'


# ----------------------------------------------
# --------       Primitives          -----------
# ----------------------------------------------

booleanType = PrimitiveType('Boolean')
intType = PrimitiveType('Int')
stringType = PrimitiveType('String')
floatType = PrimitiveType('Float')
unitType = PrimitiveType('Unit')
anyType = AnyType()
emptyVectorType = VectorType(anyType, [0])

arithmeticTypeTable = {
    intType: {
        intType: intType,
        floatType: floatType
    },
    floatType: {
        intType: floatType,
        floatType: floatType
    }
}

relationalTypeTable = {
    intType: {
        intType: booleanType,
        floatType: booleanType
    },
    floatType: {
        intType: booleanType,
        floatType: booleanType
    },
    booleanType: {
        booleanType: booleanType,
    }
}

binaryOpsTypeTable = {
    '=': arithmeticTypeTable,
    '+': arithmeticTypeTable,
    '-': arithmeticTypeTable,
    '/': arithmeticTypeTable,
    '*': arithmeticTypeTable,
    '<': relationalTypeTable,
    '<=': relationalTypeTable,
    '>': relationalTypeTable,
    '>=': relationalTypeTable,
    '==': relationalTypeTable,
    '!=': relationalTypeTable
}
