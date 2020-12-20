CC = clang++
CFLAGS = -shared -fpic -lpthread 

.PHONY: all clean

all: compileRuntime
	python3 main.py $1 
	$(CC) ./build/output.o ./build/runtime.so -o ./build/executable.exe 
	./build/executable.exe 

compileRuntime: 
	echo "Compiling runtime!"
	$(CC) $(CFLAGS) runtime.cpp -o ./build/runtime.so

clean:
	find './build' -type f -exec rm {} \;
