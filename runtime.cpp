#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

// -------------------------------------------------------
//                      RUNTIME
// -------------------------------------------------------
// looks like varargs don't work!
// okay so I should probably implement things like allocatingMemory, freeingIt,
// printing a String and so on...

extern "C" void putStrLn(char* str);
extern "C" void freeString(char* str);

void formattedPrint(const char* fmt, const char* delimeter, ...) {
    va_list args;
    va_start(args, delimeter);

    while (*fmt != '\0') {
        // integer
        if (*fmt == 'i') {
            int i = va_arg(args, int);
            printf("%d %s", i, delimeter);
            // character
        } else if (*fmt == 'c') {
            char c = va_arg(args, int);
            printf("%c %s", c, delimeter);
            // float or double
        } else if (*fmt == 'f') {
            double d = va_arg(args, double);
            printf("%.2f %s", d, delimeter);
        }
        ++fmt;
    }
    printf("\n");

    va_end(args);
}

// char* formatDouble(double x) {
//     char*
// }

void freeString(char* str) { free(str); }

void putStrLn(char* str) { printf("%s\n", str); }

void print(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    formattedPrint(fmt, "|", args);
    va_end(args);
}
