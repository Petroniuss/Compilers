# control flow instruction

N = 10;
M = 20;

if(N==10)
    print "N==10";
else if(N!=10)
    print "N!=10";


if(N>5) {
    print "N>5";
}
else if(N>=0) {
    print "N>=0";
}

if(N<10) {
    print "N<10";
}
else if(N<=15)
    print "N<=15";

k = 10;
while(k>0)
    k = k - 1;

u = [1, 2, 3, "str"];


while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
}


for i = 1:N
  for j = i:M
    print i, j;
 

for i = -1:2 - N {
    if(i<=(N/16))
        print i;
    else if(i<=(N/8))
        break;
    else if(i<=(N/4))
        continue;
    else if(i<=(N/2))
        return 0;
}


{
    N = 200;
    X = 300;
}
