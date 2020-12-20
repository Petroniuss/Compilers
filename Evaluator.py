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

            ir = """
                    ; ModuleID = "examples/ir_fpadd.py"
                    target triple = "x86_64-pc-linux-gnu"
                    target datalayout = ""

                    define i32 @main()
                    {
                    entry:
                        ret i32 1
                    }
                """

            if llvmdump is True:
                print(formatMessageBoldTitle('Unoptimized IR'))
                print(str(ir))

                outputFilename = './build/output.ll'
                with open(outputFilename, 'w') as llFile:
                    llFile.write(str(ir))

            # output object code to file
            print(formatMessageBoldTitle('Object Code'))
            objectCode = self.compileToObjectCode()
            outputFilename = './build/output.o'
            with open(outputFilename, 'wb') as objFile:
                objFile.write(objectCode)

            print(f'\tWritten to {outputFilename}')

        except CompilationFailure as failure:
            failure.printTrace()

    def compileToObjectCode(self):
        """Compile previously evaluated code into an object file.
        The object file is created for the native target, and its contents are
        returned as a bytes object.
        """
        # We use the small code model here, rather than the default one
        # `jitdefault`.
        #
        # The reason is that only ELF format is supported under the `jitdefault`
        # code model on Windows. However, COFF is commonly used by compilers on
        # Windows.
        #
        # Please refer to https://github.com/numba/llvmlite/issues/181
        # for more information about this issue.
        target_machine = self.target.create_target_machine(codemodel='small')

        # Convert LLVM IR into in-memory representation
        llvmmod = llvm.parse_assembly(str(self.codegen.module))
        return target_machine.emit_object(llvmmod)
