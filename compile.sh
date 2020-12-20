#! bin/bash

python3 main.py $1 # create llvm's ir: output.ll 
# ./build/output.ll # jit interpreter
llc -filetype=obj ./build/output.ll # static compiler
clang ./build/output.o -o ./build/executable.exe # linker
./build/executable.exe # running created executable