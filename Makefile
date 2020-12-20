CC = clang++
CFLAGS = -shared -fpic -lpthread 

.PHONY: all clean

all: compileRuntime
	@python3 main.py $1 
	@echo "\033[1m\033[92m------------------------ Linker ------------------------- \033[0m"
	$(CC) ./build/output.o ./build/runtime.so -o ./build/executable.exe 
	@echo "\033[1m\033[92m------------------------ Go! ----------------------------- \033[0m"
	@./build/executable.exe 

compileRuntime: 
	@echo "\033[1m\033[92m------------------------ Compiling Runtime ------------------------- \033[0m"
	$(CC) $(CFLAGS) runtime.cpp -o ./build/runtime.so

clean:
	find './build' -type f -exec rm {} \;
