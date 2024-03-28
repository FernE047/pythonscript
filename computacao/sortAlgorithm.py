from numpy.random import shuffle

def trocaNeM(A,n,m,imprime=True):
    global trocas
    trocas+=1
    if(imprime):
        texto="troca "+str(A[n])+" e "+str(A[m])
        texto+=" - posições "+str(n)+" e "+str(m)
        print(texto)
    A[n],A[m]=A[m],A[n]

def insertionSort(A,imprime=True):
    global comparacao
    myTrocaNeM=lambda x,y:trocaNeM(A,x,y,imprime=imprime)
    i=1
    while i<len(A):
        comparacao+=1
        j=i
        while j>0 and A[j-1] > A[j]:
            comparacao+=3
            myTrocaNeM(j,j-1)
            j=j-1
        comparacao+=3
        i=i+1
    comparacao+=1
    return(A)

def selectionPythonicSort(A,imprime):
    myTrocaNeM=lambda x,y:trocaNeM(A,x,y,imprime=imprime)
    for i in range(len(A)-1):
        indexMenor=A.index(min(A[i+1:]))
        if(indexMenor!=i):
            myTrocaNeM(i,indexMenor)

def selectionSort(A,imprime):
    global comparacao
    myTrocaNeM=lambda x,y:trocaNeM(A,x,y,imprime=imprime)
    total=len(A)
    i=0
    while i<(total-1):
        comparacao+=1
        jMin=i
        j=i+1
        while j<total:
            comparacao+=1
            if(A[j]<A[jMin]):
                comparacao+=1
                jMin=j
            j+=1
        comparacao+=1
        if(jMin!=i):
            myTrocaNeM(i,jMin)
        comparacao+=1
        i+=1
    comparacao+=1

trocas=0
comparacao=0
tamanhoLista=1000
imprime=False
imprimeListas=True
lista=[a for a in range(tamanhoLista)]
shuffle(lista)
if(imprimeListas):
    print(lista,end="\n\n")
insertionSort(lista,imprime=imprime)
if(imprimeListas):
    print("\n"+str(lista))
print("\ncomparação:"+str(comparacao))
print("\ntrocas:"+str(trocas))
