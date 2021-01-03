#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

#include <functional>
#include <string>
#include <vector>

using namespace std;

extern "C" char* formatDouble(double x);

// -------------------------------------------------------
//                      RUNTIME
// -------------------------------------------------------

double add(double one, double other) { return one + other; }

double subtract(double one, double other) { return one - other; }

double mult(double one, double other) { return one * other; }

double divi(double one, double other) { return one / other; }

extern "C" {
struct NVector {
    vector<double> values;
    vector<int> dims;
    // int refcounter = 0; // not sure if I am going to implement reference
    // counting garbage collector..

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

    NVector* combineElements(NVector* other,
                             function<double(double, double)> combiner) {
        // if we were serious we should check if dimensions match
        // throw exception if they don't

        // But since we're not ..
        NVector* result = new NVector(*this);
        for (int i = 0; i < elementsNumber(); i++) {
            result->values[i] = combiner(values[i], other->values[i]);
        }
        return result;
    }

    NVector* dotAdd(NVector* other) { return combineElements(other, add); }

    NVector* dotMinus(NVector* other) {
        return combineElements(other, subtract);
    }

    NVector* dotDiv(NVector* other) { return combineElements(other, divi); }

    NVector* dotMult(NVector* other) { return combineElements(other, mult); }

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
// So if we were serious we could implement reference counting garbage
// collector.
extern "C" NVector* literalNVector(int dimsNumber, int* dims, double* values);
extern "C" void assignValue(NVector* nvector, int* dims, double value);
extern "C" double readValue(NVector* nvector, int* ranges, int rangesSize);
extern "C" NVector* readNVector(NVector* nvector, int* ranges, int rangesSize);

extern "C" NVector* ones(int dimsNumber, int* dims);
extern "C" NVector* zeros(int dimsNumber, int* dims);

extern "C" NVector* dotAdd(NVector* one, NVector* other);
extern "C" NVector* dotMinus(NVector* one, NVector* other);
extern "C" NVector* dotDiv(NVector* one, NVector* other);
extern "C" NVector* dotMult(NVector* one, NVector* other);

NVector* dotAdd(NVector* one, NVector* other) { return one->dotAdd(other); }

NVector* dotMinus(NVector* one, NVector* other) { return one->dotMinus(other); }

NVector* dotDiv(NVector* one, NVector* other) { return one->dotDiv(other); }

NVector* dotMult(NVector* one, NVector* other) { return one->dotMult(other); }

NVector* initWithValue(int dimsNumber, int* dims, double value) {
    vector<int> dimensions(dimsNumber);
    int elems = 1;
    for (int i = 0; i < dimsNumber; i++) {
        elems *= dims[i];
        dimensions[i] = dims[i];
    }
    vector<double> values(elems, value);

    return new NVector(dimensions, values);
}

NVector* ones(int dimsNumber, int* dims) {
    return initWithValue(dimsNumber, dims, 1.0);
}

NVector* zeros(int dimsNumber, int* dims) {
    return initWithValue(dimsNumber, dims, 0.0);
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

double readValue(NVector* nvector, int* ranges, int rangesSize) {
    int* dims = new int[rangesSize / 3];
    for (int i = 0; i < rangesSize / 3; i++) {
        dims[i] = ranges[3 * i];
    }
    double val = nvector->readValue(dims);
    free(dims);

    return val;
}

NVector* readNVector(NVector* nvector, int* ranges, int rangesSize) {
    // return nvector->readNVector(nvector, ranges, rangesSize);
    return nullptr;
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
