import random

def defineLimite(fator,total,add=0):
    num=0
    while(fator*num+add<=total):
        num+=1
    limite=num
    return(limite)

def entradaDeInteiro(mensagem):
    print(mensagem)
    numeroTexto=input()
    convertido=False
    while(not(convertido)):
        try:
            numero=int(numeroTexto)
            convertido=True
        except:
            print(mensagem)
            numeroTexto=input()
    return(numero)

def entradaDeSN(mensagem):
    escolha=""
    while(escolha not in ("s","n","0")):
        print(mensagem+" [s/n]")
        escolha=input()
    return(escolha)

def impressaoLista(lista):
    for fatores in lista:
        print("4*"+str(fatores[0])+"+3*"+str(fatores[1])+"+2*"+str(fatores[2])+"+1*"+str(fatores[3]))

HORAS_A=4
HORAS_B=3
HORAS_C=2
HORAS_D=1
while True:
    print("quantas horas")
    horas=int(input())
    if(horas=="0"):
        break
    while True:
        escolha=entradaDeSN("modo ficha")
        if(escolha=="0"):
            break
        modoFicha=(escolha=="s")
        fichas=1
        linhasDisposto=1
        while True:
            lista=[]
            if(modoFicha):
                fichas=entradaDeInteiro("quantas fichas")
            else:
                linhasDisposto=entradaDeInteiro("quantas linhas")
            if((fichas==0)or(linhasDisposto==0)):
                break
            aLimite=defineLimite(HORAS_A,horas)
            for a in range(aLimite):
                bLimite=defineLimite(HORAS_B,horas,add=HORAS_A*a)
                for b in range(bLimite):
                    cLimite=defineLimite(HORAS_C,horas,add=HORAS_A*a+HORAS_B*b)
                    for c in range(cLimite):
                        dLimite=defineLimite(HORAS_D,horas,add=HORAS_A*a+HORAS_B*b+HORAS_C*c)
                        for d in range(dLimite):
                            if(HORAS_A*a+HORAS_B*b+HORAS_C*c+HORAS_D*d==horas):
                                if(modoFicha):
                                    if((a+b+c+d<=fichas*25)and(a+b+c+d>=fichas*25-25)):
                                        lista.append([a,b,c,d])
                                else:
                                    if(a+b+c+d==linhasDisposto):
                                        lista.append([a,b,c,d])
            while True:
                escolha=entradaDeSN("randomizar resultados")
                if(escolha=="s"):
                    grupo=entradaDeInteiro("quantas pessoas tem no seu grupo")
                    if(grupo<=len(lista)):
                        listaPessoais=random.sample(lista,grupo)
                        impressaoLista(listaPessoais)
                        escolha=entradaDeSN("mostrar resultados pessoais")
                        if(escolha=="s"):
                            for listaPessoal in listaPessoais:
                                linhas=0
                                listaResultante=[HORAS_A for a in range(listaPessoal[0])]+[HORAS_B for a in range(listaPessoal[1])]+[HORAS_C for a in range(listaPessoal[2])]+[HORAS_D for d in range(listaPessoal[3])]
                                random.shuffle(listaResultante)
                                for elemento in listaResultante:
                                    print(elemento)
                                    linhas+=1
                                    if(linhas==25):
                                        print("outra ficha")
                                print("continuar")
                                escolha=input()
                                if(escolha=="0"):
                                    break
                    else:
                        print("a lista é menor que o grupo")
                        impressaoLista(lista)
                else:
                    break
