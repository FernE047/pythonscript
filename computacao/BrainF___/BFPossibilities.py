def transformaEmPrograma(info):
    global ELEMENTOS
    idPrograma,tamanho=info
    lista=[]
    while(idPrograma>5):
        elemento=idPrograma%6
        idPrograma=idPrograma//6
        lista.append(ELEMENTOS[elemento])
    lista.append(ELEMENTOS[idPrograma])
    while(len(lista)<tamanho):
        lista.append(ELEMENTOS[0])
    programa="".join(lista)
    return(programa)
    

def fazPrograma(idPrograma):
    idOficial=viraId(idPrograma)
    programa=transformaEmPrograma(idOficial)
    return(programa)

def viraId(num):
    tamanho=1
    heuristicaValor=0
    idOficial=0
    while True:
        total=6**tamanho
        heuristicaValor+=total
        if(num<heuristicaValor):
            return((num-idOficial,tamanho))
        else:
            idOficial+=total
        tamanho+=1

def mostraDados(dicionario):
    global programaValido
    global idPrograma
    print("")
    for a in range(min(dicionario),max(dicionario)+1):
        if(a in dicionario.keys()):
            print(programaValido,end="/")
            print(idPrograma,end="\t")
            print(a,end="\t")
            print(dicionario[a])

def testaSeAcaba(programa):
    loop=0
    for elemento in programa:
        if(elemento=="["):
            loop+=1
        elif(elemento=="]"):
            if(loop==0):
                return(-1)
            loop-=1
    return(loop)

def saiDoLoop(programa,leitura):
    quantidadeAbertura=0
    while True:
        leitura+=1
        elemento=programa[leitura]
        if(elemento=="["):
            quantidadeAbertura+=1
        if(elemento=="]"):
            if(quantidadeAbertura==0):
                break
            else:
                quantidadeAbertura-=1
    return(leitura)

def ehErro(tira,index):
    global passos
    global LIMITEEXEC
    global LIMITEPASSOS
    global LIMITEVALOR
    global ERROINES
    global impressao
    try:
        if(len(tira)>=LIMITEEXEC):
            if(not(ERROINES)):
                if(impressao):
                    print("limite de execução",end="\t")
            return(True)
        if((tira[index]>=LIMITEVALOR)or(tira[index]<=-LIMITEVALOR)):
            if(not(ERROINES)):
                if(impressao):
                    print("limite de valor excedido pelo indice "+str(index)+" : "+str(tira[index]),end="\t")
            return(True)
        if(LIMITEPASSOS>0):
            if(passos>=LIMITEPASSOS):
                if(not(ERROINES)):
                    if(impressao):
                        print("limite de passos",end="\t")
                return(True)
    except:
        return(True)
    return(False)

def execucao(programa,tira,leitura=0,index=0):
    global DEBUGFINAL
    global passos
    global LIMITEEXEC
    global LIMITEPASSOS
    global LIMITEVALOR
    global ERROINES
    ERROINES=False
    while True:
        if(ehErro(tira,index)):
            break
        elemento=programa[leitura]
        if(DEBUGFINAL):
            passos+=1
        if(elemento=="+"):
            tira[index]+=1
        elif(elemento=="-"):
            tira[index]-=1
        elif(elemento==">"):
            index+=1
            if(index>=len(tira)):
                tira.append(0)
        elif(elemento=="<"):
            if(index==0):
                tira=[0]+tira
            else:
                index-=1
        elif(elemento=="["):
            if(tira[index]):
                leituraInicial=leitura+1
                try:
                    while(tira[index]):
                        index,leitura,tira=execucao(programa,tira,leituraInicial,index)
                except:
                    ERROINES=True
            else:
                leitura=saiDoLoop(programa,leitura)
        elif(elemento=="]"):
            return((index,leitura,tira))
        leitura+=1
        if(ehErro(tira,index)):
            break
        if(leitura==len(programa)):
            break
    return(tira)

DEBUGFINAL=True
LIMITEEXEC=10**4
LIMITEVALOR=LIMITEEXEC
LIMITEPASSOS=LIMITEEXEC
impressao=False
ERROINES=False
idPrograma=0
ELEMENTOS=["+","-",">","<","[","]"]
menoresPassos={}
jaEncontrados=[]
menoresTamanho={}
programaValido=0
potLimite=10
while (programaValido<=10**potLimite):
    passos=0
    programa=fazPrograma(idPrograma)
    quantiaColcheteAberto=testaSeAcaba(programa)
    if(quantiaColcheteAberto==0):
        tira=[0]
        tira=execucao(programa,tira)
        if(impressao):
            print(programaValido,end="/")
            print(idPrograma,end="\t")
            print(programa,end="\t")
            print(tira,end="\t")
            print("passos: "+str(passos))
        if isinstance(tira,list):
            for elemento in tira:
                if(passos==LIMITEEXEC):
                    break
                if elemento not in jaEncontrados:
                    jaEncontrados.append(elemento)
                    menoresTamanho[elemento]=programa
        programaValido+=1
    idPrograma+=1
    if(idPrograma%(7*10**(potLimite-2))==0):
        mostraDados(menoresTamanho)
for a in range(min(menoresTamanho),max(menoresTamanho)+1):
    mostraDados(menoresTamanho)
