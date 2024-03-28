def testaSeAcaba(programa):
    loop=0
    for elemento in programa:
        if(elemento=="["):
            loop+=1
        elif(elemento=="]"):
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

def somaUm(num):
    num+=1
    if(num==256):
        return(0)
    return(num)

def tiraUm(num):
    num-=1
    if(num==-1):
        return(255)
    return(num)

def execucao(programa,tira,leitura=0,index=0):
    global DEBUG
    global isOut
    global passos
    while True:
        elemento=programa[leitura]
        if(DEBUGFINAL):
            passos+=1
        if(DEBUG):
            print(elemento,end=" ")
        if(elemento=="+"):
            tira[index]=somaUm(tira[index])
        elif(elemento=="-"):
            tira[index]=tiraUm(tira[index])
        elif(elemento==">"):
            index+=1
            if(index>=len(tira)):
                tira.append(0)
        elif(elemento=="<"):
            if(index==0):
                tira=[0]+tira
            else:
                index-=1
        elif(elemento==","):
            isOut=0
            tira[index]=int(input("\nentrada:"))
        elif(elemento=="."):
            if(isOut==2):
                isOut=1
                print("saida:"+str(tira[index]),end="")
            elif(isOut==1):
                print(" "+str(tira[index]),end="")
            else:
                isOut=1
                print("\nsaida:"+str(tira[index]),end="")
        elif(elemento=="["):
            if(DEBUG):
                print("")
            if(tira[index]):
                leituraInicial=leitura+1
                while(tira[index]):
                    index,leitura=execucao(programa,tira,leituraInicial,index)
            else:
                leitura=saiDoLoop(programa,leitura)
        elif(elemento=="]"):
            if(DEBUG):
                print("]")
            return((index,leitura))
        leitura+=1
        if(DEBUG):
            print(str(index)+" "+str(tira))
        if(leitura==len(programa)):
            break
    print("")
    return(tira)

DEBUG=0
DEBUGFINAL=0
while True:
    isOut=2
    passos=0
    print("escreva o programa")
    programa=input()
    if(programa=="0"):
        break
    if(programa=="DEBUG ON"):
        DEBUG=1
        DEBUGFINAL=True
        print("DEBUG ATIVADO")
    if(programa=="DEBUG OFF"):
        DEBUG=0
        DEBUGFINAL=False
        print("DEBUG DESATIVADO")
    if(programa=="DEBUG FINAL ON"):
        DEBUGFINAL=True
        print("DEBUG FINAL ATIVADO")
    if(programa=="DEBUG FINAL OFF"):
        DEBUGFINAL=False
        print("DEBUG FINAL DESATIVADO")
    if(programa.find("DEBUG")!=-1):
        continue
    quantiaColcheteAberto=testaSeAcaba(programa)
    if(quantiaColcheteAberto==0):
        tira=execucao(programa,[0])
        if(DEBUGFINAL):
            print("")
            print(programa)
            print(tira)
            print("passos: "+str(passos))
    elif(quantiaColcheteAberto<0):
        print("falta "+str(-quantiaColcheteAberto)+" colchete: [")
    else:
        print("falta "+str(quantiaColcheteAberto)+" colchete: ]")
