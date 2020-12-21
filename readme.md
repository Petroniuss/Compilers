# Compilers

Repository contains finished exercises from laboratories during `Compilers` course at AGH UST.

Untyped Matlab-like language compiled using LLVM compiler infrstructure.

Libraries used:

- Lexer and Parser (LALR) come from PLY.
- clang - for compiling shared runtime and linking it with object file produced by code generator.
- llvmlite - provides python bindings to llvm.

Dependencies:

- llvm 10.0.0 (actually I only use clang)
- ply 3.11
- llvmlite 0.35.0
