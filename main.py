import sys

from Parser import LALRParser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Failure import CompilationFailure
from CodeGenerator import LLVMCodeGenerator


def readFile():
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "./tests/ir/foo.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    return file.read()


if __name__ == '__main__':
    sourceCode = readFile()
    try:
        ast = LALRParser(sourceCode)
        TypeChecker(ast).typecheck()

        ast.printFancyTree()
        ir = LLVMCodeGenerator(ast).generateIR()
    except CompilationFailure as failure:
        failure.printTrace()
