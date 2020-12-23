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

exampleIR = """
; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare void @printHello() #1

define i32 @main() #0 {
    %tmp = add i32 1, 2
    call void () @printHello()
    ret i32 0
}
"""


class Compiler:
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        self.codegen = LLVMCodeGenerator()

        self.target = llvm.Target.from_default_triple()
        print(self.target)

    def run(self, sourceCode, optimize=True, llvmdump=True, astDump=True):
        try:
            ast = LALRParser(sourceCode)
            TypeChecker(ast).typecheck()
            if astDump is True:
                ast.printFancyTree()

            irModule = LLVMCodeGenerator().generateIR(ast)
            # irModule = exampleIR

            if llvmdump is True:
                print(formatMessageBoldTitle('Unoptimized IR'))
                print(str(irModule))

                outputFilename = './build/output.ll'
                with open(outputFilename, 'w') as llFile:
                    llFile.write(str(irModule))

            # Convert LLVM IR into in-memory representation
            llvmmod = llvm.parse_assembly(str(irModule))

            # Optimize the module
            if optimize:
                pmb = llvm.create_pass_manager_builder()
                pmb.opt_level = 2
                pm = llvm.create_module_pass_manager()
                pmb.populate(pm)
                pm.run(llvmmod)

                if llvmdump is True:
                    print(formatMessageBoldTitle('Optimized IR'))
                    print(str(llvmmod))

            outputFilename = './build/output.o'
            with open(outputFilename, 'wb') as objectFile:
                target_machine = self.target.create_target_machine(
                    codemodel='small')

                # Convert LLVM IR into in-memory representation
                objectCode = target_machine.emit_object(llvmmod)
                objectFile.write(objectCode)

        except CompilationFailure as failure:
            failure.printTrace()
