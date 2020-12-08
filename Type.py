from typing import List


class Type:
    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.type()

    def type(self):
        return unitTypeHash()

    def unifyBinary(self, other: 'Type') -> ([str], 'Type'):
        """
            When performing binary operation we get new type
        """
        t1 = self.type()
        t2 = other.type()

        if type(self) != type(other):
            return ([f"Cannot unify these two types {t1} and {t2}!"], None)

        return self.__unifyBinary(other)

    # def matches(self, other: 'Type'):
    #     if type(self) != type(other):

    def __unifyBinary(self, ops: str, other: 'Type'):
        return ([], self)


class Primitive(Type):
    """
        Primitive type like 'int'
    """

    def __init__(self, thash: str):
        self.t = thash

    def type(self):
        return self.t

    def __unifyBinary(self, ops: str, other: 'Primitive'):
        return typeCheckPrimitiveBinaryOp(ops, self, other)


class VectorType(Type):
    def __init__(self, eType: Type, size: List[int]):
        self.eType = eType
        self.size = size

    def type(self):
        return f'Vector<{self.eType.type()}>{self.size}'

    def sizesMatch(self, other: 'VectorType'):
        if self.size == other.size:
            return []

        return [f'Sizes dont match: {self.size} and {other.size}!']

    def __unifyBinary(self, ops: str, other: 'VectorType'):
        errorMsgs, unifiedType = typeCheckPrimitiveBinaryOp(
            ops, self.eType, other.eType)

        errorMsgs += self.sizesMatch(other)

        return (errorMsgs, VectorType(unifiedType, self.size) if unifiedType is not None else None)


booleanTypeHash = 'Boolean'
intTypeHash = 'Int'
stringTypeHash = 'String'
floatTypeHash = 'Float'
unitTypeHash = 'Unit'

booleanType = Primitive(booleanTypeHash)
intType = Primitive(intTypeHash)
stringType = Primitive(stringTypeHash)
floatType = Primitive(floatTypeHash)
unitType = Primitive(unitTypeHash)


def typeCheckPrimitiveBinaryOp(ops: str, t1: Type, t2: Type):
    if ops in typeTable:
        table = typeTable[ops]
        if t1 in table:
            table = table[t1]
            if t2 in table:
                return ([], table[t2])

    return ([f'Cannot unify types {t1} and {t2} via {ops} operation!'], None)


binaryOpsTypeTable = {
    intType: {
        intType: intType,
        floatType: floatType
    },
    floatType: {
        intType: floatType,
        floatType: floatType
    }
}

typeTable = {
    '=': {
        binaryOpsTypeTable
    },
    '+': {
        binaryOpsTypeTable
    },
    '-': {
        binaryOpsTypeTable
    },
    '/': {
        binaryOpsTypeTable
    },
    '*': {
        binaryOpsTypeTable
    }
}
