x = 1;
foo = 2;

if (foo == 3) 
    foo = 12;
else if (foo == 12) {
    if (x == 1) {
        foo = 2;
    } else if (x == 2) 
        foo = 2;
     else 
        foo = 3;
}
else {
    if (x == 1) {
        foo = 2;
    } else if (x == 2) 
        foo = 2;
     else 
        foo = 3;
}
