import time

#common function

def fat(m):
    res=1
    if(m>0):
        for n in range(m,0,-1):
            res*=n
    return(res)
        
def C(trajeto,pecas):
    num=fat(trajeto)
    den=fat(pecas)*fat(trajeto-pecas)
    return(int(num/den))

def Crep(trajeto,pecas):
    novoTrajeto=trajeto+pecas-1
    Total=C(novoTrajeto,pecas)
    return(Total)

def SpacePiece(space,piece):
    Total=Crep(space,piece-space)
    return(Total)




def main() -> None:
    #common variables and constants

    startTime=time.time()
    endTime=time.time()
    realTime=endTime-startTime
    levelBoard=0                    #limite:270 2 cores
    while True:
        startTime=time.time()
        sharedBoard=8*levelBoard+8
        totalBoard=9*levelBoard+9
        Total=[1,0,0,0,0]
        filas=[0,0,0,0,0]
        for pecasFora in range(4):
            for pecasDentro in range(1,5-pecasFora):
                filas[pecasFora]=Crep(levelBoard+1,pecasDentro)
        sharedMinus=[]
        for espacosOcupados in range(sharedBoard+1):
            sharedMinus.append(0)
            for pecas in range(1,5):
                sharedMinus[espacosOcupados]+=Crep(totalBoard-espacosOcupados,pecas)

    #1 color calculus

        for pecas in range(1,5):
            Total[1]+=Crep(totalBoard,pecas)

    #2 color calculus

        for ocuppied in range(5):
            for pecas in range(ocuppied,5):
                mult=1
                mult*=SpacePiece(ocuppied,pecas)
                mult*=C(sharedBoard,pecas)
                mult*=sharedMinus[ocuppied]
                mult*=filas[4-ocuppied]+1
                Total[2]+=mult

    #3 color calculus

        


            
    # Apresentação
        print("\nlevel: "+str(levelBoard))
        for elemento in Total:
            print(str(elemento))
        endTime=time.time()
        realTime=endTime-startTime
        print(str(realTime))


if __name__ == "__main__":
    main()