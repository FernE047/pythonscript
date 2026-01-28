from copy import deepcopy

def imprimeBoard(board):
    for n in range(len(board)):
        for _ in board[n]:
            print(str(board[n]),end="")
            if (n%len(board)+1-len(board)==0):
                print("")

def calcula(board,ultimo,total,imp):
    grau=qualGrau(board)
    if(grau>=4):
        total+=1
        imprimeBoard(board)
        print(total)
        print("")
    if(grau==9):
        return(total)
    for n in range(9):
        if(possivel(board,ultimo,n)):
            newBoard=deepcopy(board)
            newBoard[n]=grau+1
            total=calcula(newBoard,n,total,imp)
    return(total)

def todasAsPossibilidade(boardOriginal):
    for n in range(len(boardOriginal)):
        for m in range(len(boardOriginal[n])):
            board=deepcopy(boardOriginal)
            board[n][m]=1
            total=calcula(board,n,total,imp)
            print(",".join([n,m]))
    

total=0
matriz=[[0,0,0],[0,0,0],[0,0,0]]
print(str(todasAsPossibilidade(matriz)))
