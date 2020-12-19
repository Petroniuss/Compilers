import llvmlite.ir as ir
import llvmlite.binding as llvm

from collections import namedtuple
from ctypes import CFUNCTYPE, c_double
from enum import Enum

from CodeGenerator import LLVMCodeGenerator
from Parser import LALRParser
from TypeChecker import TypeChecker
from AstPrinter import AstPrinter
from Failure import CompilationFailure, formatMessageBoldTitle


class Evaluator:
    """Evaluator for Kaleidoscope expressions.
    Once an object is created, calls to evaluate() add new expressions to the
    module. Definitions (including externs) are only added into the IR - no
    JIT compilation occurs. When a toplevel expression is evaluated, the whole
    module is JITed and the result of the expression is returned.
    """

    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.codegen = LLVMCodeGenerator()

        self.target = llvm.Target.from_default_triple()

    def run(self, sourceCode, optimize=True, llvmdump=True, astDump=True):
        """
            Evaluate code in codestr.
            Returns None for definitions and externs, and the evaluated expression
            value for toplevel expressions.
        """
        try:
            ast = LALRParser(sourceCode)
            TypeChecker(ast).typecheck()
            if astDump is True:
                ast.printFancyTree()

            ir = LLVMCodeGenerator().generateIR(ast)

            if llvmdump is True:
                print(formatMessageBoldTitle('Unoptimized IR'))
                print(str(self.codegen.module))

        except CompilationFailure as failure:
            failure.printTrace()
