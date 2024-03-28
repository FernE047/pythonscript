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

def execucao(programa,tira,leitura=0,index=0):
    global DEBUG
    global DEBUGFINAL
    global isOut
    global passos
    global LIMITEEXEC
    global LIMITEPASSOS
    global LIMITEVALOR
    ERROINES=False
    while True:
        elemento=programa[leitura]
        if(DEBUGFINAL):
            passos+=1
        if(DEBUG):
            print(elemento,end=" ")
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
                try:
                    while(tira[index]):
                        index,leitura,tira=execucao(programa,tira,leituraInicial,index)
                except:
                    print("Erro")
                    ERROINES=True
            else:
                leitura=saiDoLoop(programa,leitura)
        elif(elemento=="]"):
            return((index,leitura,tira))
        if(len(tira)>=LIMITEEXEC):
            if(not(ERROINES)):
                print("limite de execução")
            break
        if((tira[index]>=LIMITEVALOR)or(tira[index]<=-LIMITEVALOR)):
            if(not(ERROINES)):
                print("limite de valor excedido pelo indice:")
                print(index)
                print("valor:")
                print(tira[index])
            break
        if(DEBUGFINAL):
            if(LIMITEPASSOS>0):
                if(passos>=LIMITEPASSOS):
                    if(not(ERROINES)):
                        print("limite de passos")
                    break
        leitura+=1
        if(DEBUG):
            print(str(index)+" "+str(tira))
        if(leitura==len(programa)):
            break
    print("")
    return(tira)

DEBUG=0
DEBUGFINAL=0
LIMITEEXEC=10**4
LIMITEVALOR=LIMITEEXEC
LIMITEPASSOS=0
while True:
    isOut=2
    passos=0
    print("escreva o programa")
    programa=input()
    if(programa.find("DEBUG")!=-1):
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
        if(programa.find("DEBUG LIMITE PASSOS ")!=-1):
            LIMITEPASSOS=int(programa[20:])
            print("LIMITEPASSOS="+str(LIMITEPASSOS))
            print("DEBUG FINAL ATIVADO")
            DEBUGFINAL=True
        elif(programa.find("DEBUG LIMITE VALOR ")!=-1):
            LIMITEVALOR=int(programa[19:])
            print("LIMITEVALOR="+str(LIMITEVALOR))
        elif(programa.find("DEBUG LIMITE ")!=-1):
            LIMITEEXEC=int(programa[13:])
            print("LIMITEEXEC="+str(LIMITEEXEC))
        elif(programa.find("DEBUG LIMITES ")!=-1):
            limites=int(programa[14:])
            LIMITEEXEC=limites
            LIMITEPASSOS=limites
            LIMITEVALOR=limites
            print("LIMITEEXEC="+str(LIMITEEXEC))
            print("LIMITEVALOR="+str(LIMITEVALOR))
            print("LIMITEPASSOS="+str(LIMITEPASSOS))
            print("DEBUG FINAL ATIVADO")
            DEBUGFINAL=True
        continue
    elif(programa=="0"):
        break
    quantiaColcheteAberto=testaSeAcaba(programa)
    tira=[0]
    if(quantiaColcheteAberto==0):
        tira=execucao(programa,tira)
        if(DEBUGFINAL):
            print("")
            print(programa)
            print(tira)
            print("passos: "+str(passos))
    elif(quantiaColcheteAberto<0):
        print("falta "+str(-quantiaColcheteAberto)+" colchete: [")
    else:
        print("falta "+str(quantiaColcheteAberto)+" colchete: ]")
