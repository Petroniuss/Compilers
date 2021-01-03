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