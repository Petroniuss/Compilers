x = 1.0;
z = ones(3, 3);

while (x <= 12.0) {
    print x;
    x = x * 1.2;
    z = z + z;
}

# If you comment this line optimizer will inline the above loop
print z;

# It's actually pretty hard to write a loop that optimizer doesn't inline 
# If I were to run optimizer on linked code it would probably look a lot different!
# We can see that since we're generating calls to runtime 
# (which optimizer isn't aware of) and so it cannot eliminate these calls (even though they're redundant).

# So in order to get the most performant code we should:
#  - emit llvm ir from cpp runtime (using clang++)
#  - link it with ir generated by my front-end compiler (using llvm) 
#  - run optimizer on linked ir and then finally emit executable.