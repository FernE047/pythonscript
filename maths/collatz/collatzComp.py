def collatz(termo,grau):
    passos=0
    if(grau==0):
        while(termo!=1):
            if((termo%2)==0):
                termo/=2
            else:
                termo=3*termo+1
            passos+=1
    elif(grau==1):
        while(termo!=1):
            if((termo%2)==0):
                termo/=2
            elif((termo%4)==3):
                termo=(3*termo+1)/2
            elif((termo%8)==1):
                termo=(3*termo+1)/2
            else:
                termo=(termo-1)/4
            passos+=1
    elif(grau==2):
        while(termo!=1):
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
    return(passos)

limite=0
while(limite==0):
    print("digite inicial e o limite separado por enter")
    inicial=(int(input()))
    if(inicial<=0):
        continue
    limite=(int(input())+1)
if(inicial>limite-1):  #inverte valores
    limite+=inicial
    print(str(limite))
    inicial=limite-inicial-1
    print(str(inicial))
    limite-=inicial
    print(str(limite))
for fruto in range(inicial,limite):
    passos=[collatz(fruto,i) for i in range(3)]
    print("{0:5d}:{1:4d},{2:4d},{3:4d}".format(fruto,passos[0],passos[1],passos[2]))
    
