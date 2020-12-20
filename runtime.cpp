#include <stdio.h>
#include <stdlib.h>

using namespace std;

// -------------------------------------------------------
//                      RUNTIME
// -------------------------------------------------------

extern "C" void printHello();

void printHello() { printf("Hello from runtime!\n"); }
