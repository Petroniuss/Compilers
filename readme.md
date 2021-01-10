# Compilers

Repository contains finished project completed during `Compilers` course at AGH UST.

Statically-typed Matlab-like language compiled using LLVM compiler infrastracture.

## Example program

See [Usage example](#Usage-example) below to see generated ir for this code.

Code:

```
M = zeros(3, 3);
print M;


# Assigining individual values works!
M[1, 1] = 69.0;

# Reading values works!
x = M[1, 1];
print "x =", x;

X = [1, 2, 3];
for i = 0:2 {
    M[i, i] = X[i];
}

print M;
```

Output:

```
[    0.00,     0.00,     0.00    ]
[    0.00,     0.00,     0.00    ]
[    0.00,     0.00,     0.00    ]

x =   69.00
[    1.00,     0.00,     0.00    ]
[    0.00,     2.00,     0.00    ]
[    0.00,     0.00,     3.00    ]
```

## Usage example

Makefile prints AST, both unoptimized and optimized IR and generates executable file which is automatically executed.

Command:

```
make all arg=./tests/ir/slice.m
```

Output:

```
------------------------ Compiling Runtime -------------------------
clang++ -shared -fpic -lpthread  runtime.cpp -o ./build/runtime.so
------------------------ Compiler -------------------------
<Target x86-64 (64-bit X86: EM64T and AMD64)>
------------------------ Compiling ./tests/ir/slice.m  ------------------------
M = zeros(3, 3);
print M;


# Assigining individual values works!
M[1, 1] = 69.0;

# Reading values works!
x = M[1, 1];
print "x =", x;

X = [1, 2, 3];
for i = 0:2 {
    M[i, i] = X[i];
}

print M;
------------------------ Abstract Syntax Tree  ------------------------
Root
└── CodeBlock
    ├── =
    │   ├── FunctionCall
    │   │   ├── Int
    │   │   │   └── 3
    │   │   ├── Int
    │   │   │   └── 3
    │   │   └── zeros
    │   └── ID
    │       └── M
    ├── =
    │   ├── Float
    │   │   └── 69.0
    │   └── VectorSlice
    │       ├── ID
    │       │   └── M
    │       ├── SimpleRange
    │       │   └── Int
    │       │       └── 1
    │       └── SimpleRange
    │           └── Int
    │               └── 1
    ├── =
    │   ├── ID
    │   │   └── x
    │   └── VectorSlice
    │       ├── ID
    │       │   └── M
    │       ├── SimpleRange
    │       │   └── Int
    │       │       └── 1
    │       └── SimpleRange
    │           └── Int
    │               └── 1
    ├── =
    │   ├── ID
    │   │   └── X
    │   └── Vector
    │       ├── Int
    │       │   └── 1
    │       ├── Int
    │       │   └── 2
    │       └── Int
    │           └── 3
    ├── For
    │   ├── CodeBlock
    │   │   └── =
    │   │       ├── VectorSlice
    │   │       │   ├── ID
    │   │       │   │   └── M
    │   │       │   ├── SimpleRange
    │   │       │   │   └── ID
    │   │       │   │       └── i
    │   │       │   └── SimpleRange
    │   │       │       └── ID
    │   │       │           └── i
    │   │       └── VectorSlice
    │   │           ├── ID
    │   │           │   └── X
    │   │           └── SimpleRange
    │   │               └── ID
    │   │                   └── i
    │   ├── ID
    │   │   └── i
    │   └── Range
    │       ├── Int
    │       │   └── 0
    │       └── Int
    │           └── 2
    ├── FunctionCall
    │   ├── ID
    │   │   └── M
    │   └── print
    ├── FunctionCall
    │   ├── ID
    │   │   └── x
    │   ├── String
    │   │   └── x =
    │   └── print
    └── FunctionCall
        ├── ID
        │   └── M
        └── print

------------------------ Unoptimized IR  ------------------------
; ModuleID = "Main"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i8* @"formatInt"(i32 %".1")

declare i8* @"formatDouble"(double %".1")

declare void @"freeString"(i8* %".1")

declare void @"putLn"()

declare void @"putStrLn"(i8* %".1")

declare void @"putVectorLn"({}* %".1")

declare void @"putStr"(i8* %".1")

declare {}* @"zeros"(i32 %".1", i32* %".2")

declare {}* @"ones"(i32 %".1", i32* %".2")

declare {}* @"dotAdd"({}* %".1", {}* %".2")

declare {}* @"dotMinus"({}* %".1", {}* %".2")

declare {}* @"dotMult"({}* %".1", {}* %".2")

declare {}* @"dotDiv"({}* %".1", {}* %".2")

declare void @"assignValue"({}* %".1", i32* %".2", i32 %".3", double %".4")

declare double @"readValue"({}* %".1", i32* %".2", i32 %".3")

declare {}* @"literalNVector"(i32 %".1", i32* %".2", double* %".3")

define i32 @"main"()
{
entry:
  %".2" = alloca [2 x i32]
  %".3" = getelementptr [2 x i32], [2 x i32]* %".2", i32 0, i32 0
  store i32 3, i32* %".3"
  %".5" = getelementptr [2 x i32], [2 x i32]* %".2", i32 0, i32 1
  store i32 3, i32* %".5"
  %".7" = getelementptr [2 x i32], [2 x i32]* %".2", i32 0, i32 0
  %".8" = call {}* @"zeros"(i32 2, i32* %".7")
  %"M" = alloca {}*
  store {}* %".8", {}** %"M"
  %".10" = load {}*, {}** %"M"
  call void @"putVectorLn"({}* %".10")
  call void @"putLn"()
  %".13" = alloca [6 x i32]
  %".14" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 0
  store i32 1, i32* %".14"
  %".16" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 1
  store i32 1, i32* %".16"
  %".18" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 2
  store i32 0, i32* %".18"
  %".20" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 3
  store i32 1, i32* %".20"
  %".22" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 4
  store i32 1, i32* %".22"
  %".24" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 5
  store i32 0, i32* %".24"
  %".26" = load {}*, {}** %"M"
  %".27" = getelementptr [6 x i32], [6 x i32]* %".13", i32 0, i32 0
  call void @"assignValue"({}* %".26", i32* %".27", i32 6, double 0x4051400000000000)
  %".29" = alloca [6 x i32]
  %".30" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 0
  store i32 1, i32* %".30"
  %".32" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 1
  store i32 1, i32* %".32"
  %".34" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 2
  store i32 0, i32* %".34"
  %".36" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 3
  store i32 1, i32* %".36"
  %".38" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 4
  store i32 1, i32* %".38"
  %".40" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 5
  store i32 0, i32* %".40"
  %".42" = load {}*, {}** %"M"
  %".43" = getelementptr [6 x i32], [6 x i32]* %".29", i32 0, i32 0
  %".44" = call double @"readValue"({}* %".42", i32* %".43", i32 6)
  %"x" = alloca double
  store double %".44", double* %"x"
  call void @"putStr"(i8* getelementptr ([4 x i8], [4 x i8]* @"global_0", i32 0, i32 0))
  %".47" = load double, double* %"x"
  %".48" = call i8* @"formatDouble"(double %".47")
  call void @"putStr"(i8* %".48")
  call void @"freeString"(i8* %".48")
  call void @"putLn"()
  %".52" = sitofp i32 1 to double
  %".53" = getelementptr [3 x double], [3 x double]* @"global_1", i32 0, i32 0
  store double %".52", double* %".53"
  %".55" = sitofp i32 2 to double
  %".56" = getelementptr [3 x double], [3 x double]* @"global_1", i32 0, i32 1
  store double %".55", double* %".56"
  %".58" = sitofp i32 3 to double
  %".59" = getelementptr [3 x double], [3 x double]* @"global_1", i32 0, i32 2
  store double %".58", double* %".59"
  %".61" = call {}* @"literalNVector"(i32 1, i32* getelementptr ([1 x i32], [1 x i32]* @"global_2", i32 0, i32 0), double* getelementptr ([3 x double], [3 x double]* @"global_1", i32 0, i32 0))
  %"X" = alloca {}*
  store {}* %".61", {}** %"X"
  br label %"for-init-block"
for-init-block:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"for-condition"
for-condition:
  %".66" = load i32, i32* %"i"
  %".67" = sitofp i32 %".66" to double
  %".68" = sitofp i32 2 to double
  %"for-cmp" = fcmp ule double %".67", %".68"
  br i1 %"for-cmp", label %"for-body-block", label %"for-merged"
for-body-block:
  %".70" = alloca [3 x i32]
  %".71" = load i32, i32* %"i"
  %".72" = getelementptr [3 x i32], [3 x i32]* %".70", i32 0, i32 0
  store i32 %".71", i32* %".72"
  %".74" = getelementptr [3 x i32], [3 x i32]* %".70", i32 0, i32 1
  store i32 %".71", i32* %".74"
  %".76" = getelementptr [3 x i32], [3 x i32]* %".70", i32 0, i32 2
  store i32 0, i32* %".76"
  %".78" = load {}*, {}** %"X"
  %".79" = getelementptr [3 x i32], [3 x i32]* %".70", i32 0, i32 0
  %".80" = call double @"readValue"({}* %".78", i32* %".79", i32 3)
  %".81" = alloca [6 x i32]
  %".82" = load i32, i32* %"i"
  %".83" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 0
  store i32 %".82", i32* %".83"
  %".85" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 1
  store i32 %".82", i32* %".85"
  %".87" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 2
  store i32 0, i32* %".87"
  %".89" = load i32, i32* %"i"
  %".90" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 3
  store i32 %".89", i32* %".90"
  %".92" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 4
  store i32 %".89", i32* %".92"
  %".94" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 5
  store i32 0, i32* %".94"
  %".96" = load {}*, {}** %"M"
  %".97" = getelementptr [6 x i32], [6 x i32]* %".81", i32 0, i32 0
  call void @"assignValue"({}* %".96", i32* %".97", i32 6, double %".80")
  %".99" = load i32, i32* %"i"
  %".100" = add i32 %".99", 1
  store i32 %".100", i32* %"i"
  br label %"for-condition"
for-merged:
  %".103" = load {}*, {}** %"M"
  call void @"putVectorLn"({}* %".103")
  call void @"putLn"()
  ret i32 0
}

@"global_0" = constant [4 x i8] [i8 120, i8 32, i8 61, i8 0]
@"global_1" = global [3 x double] [double              0x0, double              0x0, double              0x0]
@"global_2" = constant [1 x i32] [i32 3]
------------------------ Optimized IR  ------------------------
; ModuleID = '<string>'
source_filename = "<string>"
target triple = "unknown-unknown-unknown"

@global_0 = constant [4 x i8] c"x =\00"
@global_1 = global [3 x double] zeroinitializer
@global_2 = constant [1 x i32] [i32 3]

declare i8* @formatDouble(double) local_unnamed_addr

declare void @freeString(i8*) local_unnamed_addr

declare void @putLn() local_unnamed_addr

declare void @putVectorLn({}*) local_unnamed_addr

declare void @putStr(i8*) local_unnamed_addr

declare {}* @zeros(i32, i32*) local_unnamed_addr

declare void @assignValue({}*, i32*, i32, double) local_unnamed_addr

declare double @readValue({}*, i32*, i32) local_unnamed_addr

declare {}* @literalNVector(i32, i32*, double*) local_unnamed_addr

define i32 @main() local_unnamed_addr {
entry:
  %.2 = alloca [2 x i32], align 4
  %.3 = getelementptr inbounds [2 x i32], [2 x i32]* %.2, i64 0, i64 0
  store i32 3, i32* %.3, align 4
  %.5 = getelementptr inbounds [2 x i32], [2 x i32]* %.2, i64 0, i64 1
  store i32 3, i32* %.5, align 4
  %.8 = call {}* @zeros(i32 2, i32* nonnull %.3)
  call void @putVectorLn({}* %.8)
  call void @putLn()
  %.13 = alloca [6 x i32], align 4
  %.14 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 0
  store i32 1, i32* %.14, align 4
  %.16 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 1
  store i32 1, i32* %.16, align 4
  %.18 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 2
  store i32 0, i32* %.18, align 4
  %.20 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 3
  store i32 1, i32* %.20, align 4
  %.22 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 4
  store i32 1, i32* %.22, align 4
  %.24 = getelementptr inbounds [6 x i32], [6 x i32]* %.13, i64 0, i64 5
  store i32 0, i32* %.24, align 4
  call void @assignValue({}* %.8, i32* nonnull %.14, i32 6, double 6.900000e+01)
  %.29 = alloca [6 x i32], align 4
  %.30 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 0
  store i32 1, i32* %.30, align 4
  %.32 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 1
  store i32 1, i32* %.32, align 4
  %.34 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 2
  store i32 0, i32* %.34, align 4
  %.36 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 3
  store i32 1, i32* %.36, align 4
  %.38 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 4
  store i32 1, i32* %.38, align 4
  %.40 = getelementptr inbounds [6 x i32], [6 x i32]* %.29, i64 0, i64 5
  store i32 0, i32* %.40, align 4
  %.44 = call double @readValue({}* %.8, i32* nonnull %.30, i32 6)
  call void @putStr(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @global_0, i64 0, i64 0))
  %.48 = call i8* @formatDouble(double %.44)
  call void @putStr(i8* %.48)
  call void @freeString(i8* %.48)
  call void @putLn()
  store double 1.000000e+00, double* getelementptr inbounds ([3 x double], [3 x double]* @global_1, i64 0, i64 0), align 16
  store double 2.000000e+00, double* getelementptr inbounds ([3 x double], [3 x double]* @global_1, i64 0, i64 1), align 8
  store double 3.000000e+00, double* getelementptr inbounds ([3 x double], [3 x double]* @global_1, i64 0, i64 2), align 16
  %.61 = call {}* @literalNVector(i32 1, i32* getelementptr inbounds ([1 x i32], [1 x i32]* @global_2, i64 0, i64 0), double* getelementptr inbounds ([3 x double], [3 x double]* @global_1, i64 0, i64 0))
  %.70 = alloca [3 x i32], align 4
  %.72 = getelementptr inbounds [3 x i32], [3 x i32]* %.70, i64 0, i64 0
  store i32 0, i32* %.72, align 4
  %.74 = getelementptr inbounds [3 x i32], [3 x i32]* %.70, i64 0, i64 1
  store i32 0, i32* %.74, align 4
  %.76 = getelementptr inbounds [3 x i32], [3 x i32]* %.70, i64 0, i64 2
  store i32 0, i32* %.76, align 4
  %.80 = call double @readValue({}* %.61, i32* nonnull %.72, i32 3)
  %.81 = alloca [6 x i32], align 4
  %.83 = getelementptr inbounds [6 x i32], [6 x i32]* %.81, i64 0, i64 0
  %0 = bitcast [6 x i32]* %.81 to i8*
  call void @llvm.memset.p0i8.i64(i8* nonnull align 4 dereferenceable(24) %0, i8 0, i64 24, i1 false)
  call void @assignValue({}* %.8, i32* nonnull %.83, i32 6, double %.80)
  %.70.1 = alloca [3 x i32], align 4
  %.72.1 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.1, i64 0, i64 0
  store i32 1, i32* %.72.1, align 4
  %.74.1 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.1, i64 0, i64 1
  store i32 1, i32* %.74.1, align 4
  %.76.1 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.1, i64 0, i64 2
  store i32 0, i32* %.76.1, align 4
  %.80.1 = call double @readValue({}* %.61, i32* nonnull %.72.1, i32 3)
  %.81.1 = alloca [6 x i32], align 4
  %.83.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 0
  store i32 1, i32* %.83.1, align 4
  %.85.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 1
  store i32 1, i32* %.85.1, align 4
  %.87.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 2
  store i32 0, i32* %.87.1, align 4
  %.90.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 3
  store i32 1, i32* %.90.1, align 4
  %.92.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 4
  store i32 1, i32* %.92.1, align 4
  %.94.1 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.1, i64 0, i64 5
  store i32 0, i32* %.94.1, align 4
  call void @assignValue({}* %.8, i32* nonnull %.83.1, i32 6, double %.80.1)
  %.70.2 = alloca [3 x i32], align 4
  %.72.2 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.2, i64 0, i64 0
  store i32 2, i32* %.72.2, align 4
  %.74.2 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.2, i64 0, i64 1
  store i32 2, i32* %.74.2, align 4
  %.76.2 = getelementptr inbounds [3 x i32], [3 x i32]* %.70.2, i64 0, i64 2
  store i32 0, i32* %.76.2, align 4
  %.80.2 = call double @readValue({}* %.61, i32* nonnull %.72.2, i32 3)
  %.81.2 = alloca [6 x i32], align 4
  %.83.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 0
  store i32 2, i32* %.83.2, align 4
  %.85.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 1
  store i32 2, i32* %.85.2, align 4
  %.87.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 2
  store i32 0, i32* %.87.2, align 4
  %.90.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 3
  store i32 2, i32* %.90.2, align 4
  %.92.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 4
  store i32 2, i32* %.92.2, align 4
  %.94.2 = getelementptr inbounds [6 x i32], [6 x i32]* %.81.2, i64 0, i64 5
  store i32 0, i32* %.94.2, align 4
  call void @assignValue({}* %.8, i32* nonnull %.83.2, i32 6, double %.80.2)
  call void @putVectorLn({}* %.8)
  call void @putLn()
  ret i32 0
}

; Function Attrs: argmemonly nounwind willreturn
declare void @llvm.memset.p0i8.i64(i8* nocapture writeonly, i8, i64, i1 immarg) #0

attributes #0 = { argmemonly nounwind willreturn }

------------------------ Linker -------------------------
clang++ ./build/output.o ./build/runtime.so -o ./build/executable.exe
------------------------ Go! -----------------------------
[    0.00,     0.00,     0.00    ]
[    0.00,     0.00,     0.00    ]
[    0.00,     0.00,     0.00    ]

x =   69.00
[    1.00,     0.00,     0.00    ]
[    0.00,     2.00,     0.00    ]
[    0.00,     0.00,     3.00    ]

```

## Libraries used:

- Lexer and Parser (LALR) come from PLY.
- clang - for compiling shared runtime and linking it with object file produced by code generator.
- llvmlite - provides python bindings to llvm.

## Dependencies:

- llvm 10.0.0 (actually I only use clang)
- ply 3.11
- llvmlite 0.35.0
