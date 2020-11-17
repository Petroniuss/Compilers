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

for i = 1:N
  for j = i:M
    print i, j;