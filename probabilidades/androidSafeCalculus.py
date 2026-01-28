
def qualGrau(board):
    grau=0
    for n in board:
        if(n):
            grau+=1
    return grau

def copiaLista(lista):
    listaNova=[]
    for n in lista:
        listaNova.append(n)
    return listaNova

def identificaCanto(canto):
    if(canto==0):
        return 0
    elif(canto==2):
        return 1
    elif(canto==6):
        return 2
    elif(canto==8):
        return 3

def imprimeBoard(board):
    for n in range(9):
        print(str(board[n]),end="")
        if (n%3==2):
            print("")

def possivel(board,ultimo,proximo):
    if(board[proximo]):
        return False
    if(ultimo==proximo):
        return False
    if((proximo==4)or(ultimo==4)):
        return True
    oposto=(8,7,6,5,4,3,2,1,0)
    if(proximo in (1,3,5,7)):
        if(board[4]):
            return True
        elif(ultimo==oposto[proximo]):
            return False
        else:
            return True
    else:
        if(ultimo in (1,3,5,7)):
            return True
        elif(ultimo==oposto[proximo]):
            if(board[4]):
                return True
            else:
                return False
        else:
            horizontal=(2,0,8,6)
            vertical=(6,8,0,2)
            obstaculos=((1,3),(1,5),(7,3),(7,5))
            cantoDestino=identificaCanto(proximo)
            if(ultimo==vertical[cantoDestino]):
                if(board[obstaculos[cantoDestino][1]]):
                    return True
                else:
                    return False
            elif(ultimo==horizontal[cantoDestino]):
                if(board[obstaculos[cantoDestino][0]]):
                    return True
                else:
                    return False        
    
def calcula(board,ultimo,total,imp):
    grau=qualGrau(board)
    if(grau>=4):
        total+=1
        if(imp):
            imprimeBoard(board)
            print(total)
            print("")
    if(grau==9):
        return(total)
    for n in range(9):
        if(possivel(board,ultimo,n)):
            newBoard=copiaLista(board)
            newBoard[n]=grau+1
            total=calcula(newBoard,n,total,imp)
    return(total)

total=0
for n in range(9):
    boardOriginal=[0,0,0,0,0,0,0,0,0]
    boardOriginal[n]=1
    imp=False
    total=calcula(boardOriginal,n,total,imp)
    print(n)
print(str(total))
