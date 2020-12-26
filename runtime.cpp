#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

#include <string>
#include <vector>

using namespace std;

extern "C" char* formatDouble(double x);

// -------------------------------------------------------
//                      RUNTIME
// -------------------------------------------------------

extern "C" {
struct NVector {
    vector<double> values;
    vector<int> dims;
    // int refcounter = 0; // not sure if I am going to implement this bit

    NVector(vector<int> dimsVector, vector<double> valuesVector)
        : values(valuesVector), dims(dimsVector) {}

    int dimensionsNumber() { return dims.size(); }

    int flatIndex(int* indices) {
        int index = 0;
        int cnter = 1;
        for (int i = dimensionsNumber() - 1; i >= 0; i--) {
            int dimSize = dims[i];
            int dimIndex = indices[i];
            index += dimIndex * cnter;
            cnter *= dimSize;
        }

        return index;
    }

    int elementsNumber() {
        int counter = 1;
        for (int dim : dims) {
            counter *= dim;
        }

        return counter;
    }

    void assignValue(int* indices, double value) {
        const int index = flatIndex(indices);
        values[index] = value;
    }

    double readValue(int* indices) {
        const int index = flatIndex(indices);

        return values[index];
    }

    void print() {
        int index = -1;
        if (dimensionsNumber() == 2) {
            for (int i = 0; i < dims[0]; i++) {
                printf("[");
                for (int j = 0; j < dims[1]; j++) {
                    index += 1;
                    double value = values[index];
                    char* formatted = formatDouble(value);

                    printf("%s", formatted);
                    if (j != dims[1] - 1) {
                        printf(", ");
                    }

                    free(formatted);
                }
                printf("    ]\n");
            }
        } else {
            printf("[ ");
            int count = elementsNumber();
            for (int i = 0; i < count; i++) {
                index += 1;
                double value = values[index];
                char* formatted = formatDouble(value);

                printf("%s", formatted);
                if (i != count - 1) {
                    printf(", ");
                }

                free(formatted);
            }
            printf("   ]");
        }
    }

} typedef NVector;
}

// --------------------- print ---------------------------
extern "C" void putStr(char* str);
extern "C" void putStrLn(char* str);
extern "C" void putLn();
extern "C" void putVectorLn(NVector* nvector);

// -------------------- strings ---------------------------
extern "C" char* formatInt(int x);
extern "C" void freeString(char* str);
extern "C" char* formatDouble(double x);
extern "C" char* formatInt(int x);
extern "C" void freeString(char* str);

// --------------------- vectors ---------------------------
// Note that they're allocated on the heap!
extern "C" NVector* literalNVector(int dimsNumber, int* dims, double* values);
extern "C" void assignValue(NVector* nvector, int* dims, double value);
extern "C" double readValue(NVector* nvector, int* dims);
// extern "C" int* allocIntArray
extern "C" NVector* ones(int dimsNumber, int* dims);

NVector* ones(int dimsNumber, int* dims) {
    // ez ...
    return nullptr;
}

NVector* literalNVector(int dimsNumber, int* dims, double* values) {
    int elementCount = 1;
    vector<int> dimsVector(dimsNumber);
    for (int i = 0; i < dimsNumber; i++) {
        dimsVector[i] = dims[i];
        elementCount *= dims[i];
    }

    vector<double> valuesVector(elementCount);

    for (int i = 0; i < elementCount; i++) {
        valuesVector[i] = values[i];
    }

    return new NVector(dimsVector, valuesVector);
}

void putVectorLn(NVector* nvector) { nvector->print(); }

void assignValue(NVector* nvector, int* dims, double value) {
    nvector->assignValue(dims, value);
}

double readValue(NVector* nvector, int* dims) {
    return nvector->readValue(dims);
}

char* formatDouble(double x) {
    int space = 8;
    char* buffer = (char*)malloc(sizeof(char) * (space + 12));
    sprintf(buffer, "%*.2f", space, x);

    return buffer;
}

char* formatInt(int x) {
    int space = 8;
    char* buffer = (char*)malloc(sizeof(char) * (space + 12));
    sprintf(buffer, "%*d", space, x);

    return buffer;
}

void freeString(char* str) { free(str); }

void putStrLn(char* str) { printf("%s\n", str); }

void putStr(char* str) { printf("%s", str); }

void putLn() { printf("\n"); }
