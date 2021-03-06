A = zeros(7, 7);  # create 5x5 matrix filled with zeros
B = ones(7, 7);   # create 7x7 matrix filled with ones
I = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere
D1 = A.+(B') ; # add element-wise A with transpose of B
D2 -= A.-(B') ; # substract element-wise A with transpose of B
D3 *= A.*(B') ; # multiply element-wise A with transpose of B
D4 /= A./(B)' ; # divide element-wise A with transpose of B

E1 = [ [ 1, 2, 3],
       [ 4, 5, 6],
       [ 7, 8, 9] ];

__x = "s";
_1_ = "s";


# ___ = 12;  # This is invalid
# 12_ = "x"; # also invalid

# res0 = .   # such lexem invalid
res1 = 60.500;
res2 = 60.;
res3 = .500;
res4 = 60.52E2;
str = "Hello world";

if (m==n) { 
    if (m >= n) 
        print res;
}


# Few edge cases:
# "foo"                             # 1. String after a comment.
X = "\"\"";                         # 2. Escaping (") char within a string.
Y = "Hash # Hash";                   # 3. Hash within a string.
Z = " $ $2jrj fa0s9jt \n ala \n";   # 4. String with newline characters.