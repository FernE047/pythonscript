def collatz(termo,grau):
    passos=0
    if(grau==0):
        print("\ncollatz nivel 0:\n")
        while(termo!=1):
            print(str(int(termo)))
            if((termo%2)==0):
                termo/=2
            else:
                termo=3*termo+1
            passos+=1
    elif(grau==1):
        print("\ncollatz nivel 1:\n")
        while(termo!=1):
            print(str(int(termo)))
            if((termo%2)==0):
                termo/=2
            elif((termo%4)==3):
                termo=(3*termo+1)/2
            elif((termo%8)==1):
                termo=(3*termo+1)/4
            else:
                termo=(termo-1)/4
            passos+=1
    elif(grau==2):
        print("\ncollatz nivel 2:\n")
        while(termo!=1):
            print(str(int(termo)))
            if(termo%2==0):
                termo/=2
            elif(termo%8==5):
                termo=(termo-1)/4
            elif(termo%8==7):
                termo=(3*termo+1)/2
            elif(termo%16==3):
                termo=(termo-1)/2
            elif(termo%16==9):
                termo=(3*termo+1)/4
            elif(termo%16==11):
                termo=(3*termo+1)/2
            elif(termo%32==1):
                termo=(3*termo+1)/4
            elif(termo%64==17):
                termo=(3*termo-3)/16
            elif(termo%128==49):
                termo=(3*termo-3)/16
            elif(termo%128==113):
                termo=(termo-17)/32
            passos+=1
    print(str(int(termo)))
    return(int(passos))
    

fruto=1
passos=[0 for i in range(2)]
while(fruto!=0):
    passos=[collatz(fruto,i) for i in range(3)]
    print(f"passos:{passos[0]:4d},{passos[1]:4d},{passos[2]:4d}\n")
    fruto=int(input())


