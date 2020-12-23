#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

// -------------------------------------------------------
//                      RUNTIME
// -------------------------------------------------------

extern "C" void putStr(char* str);
extern "C" void putStrLn(char* str);
extern "C" void putLn();

extern "C" char* formatDouble(double x);
extern "C" void freeString(char* str);

char* formatDouble(double x) {
    int space = 8;
    char* buffer = (char*)malloc(sizeof(char) * (space + 12));
    sprintf(buffer, "%*.2f", space, x);

    return buffer;
}

void freeString(char* str) { free(str); }

void putStrLn(char* str) { printf("%s\n", str); }

void putStr(char* str) { printf("%s", str); }

void putLn() { printf("\n"); }
