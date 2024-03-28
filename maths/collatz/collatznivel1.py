semente=1
while(semente!=0):
    quant=1
    while((semente%8)==5):
        semente=(semente-1)/4
        quant+=1
    termo=semente
    if quant<10:
        quant=10
    if(termo%2):
        for a in range(1,quant):
            termo=4*termo+1
        for a in range(1,quant+1):
            print(str(int(termo)),end="")
            if((termo%6)==1):
                print(" < "+str(int((4*termo-1)/3)),end="")
            elif((termo%6)==5):
                print(" < "+str(int((2*termo-1)/3)),end="")
            print("\nV")
            if(termo!=semente):
                termo=(termo-1)/4
    else:
        print(str(int(termo)))
        while((termo%2)==0):
            termo/=2
            print("V\n"+str(int(termo)))
    if((semente%4)==3):
        print(str(int((3*semente+1)/2)))
    elif((semente%8)==1):
        print(str(int((3*semente+1)/4)))
    semente=int(input())
    
