#! bin/bash

# write a script that takes a file and produces object file and links it using gcc

if [ -z "$1" ] 
  then
    python3 main.py $1
    clang ./build/output.o -o executable.exe
fi