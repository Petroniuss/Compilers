#! bin/bash

# write a script that takes a file and produces object file and links it using gcc

python3 main.py $1
llc ./build/output.ll
clang ./build/output.s -o ./build/executable.exe