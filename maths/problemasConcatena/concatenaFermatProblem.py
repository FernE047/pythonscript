from time import time
from textos import embelezeTempo

def pos(a,pot):
        respostas=[]
        a=a**pot
        for b in range(1,a):
                bPot=b**pot
                textB=str(bPot)
                for c in range(a):
                        cPot=c**pot
                        textC=str(cPot)
                        textNum=textB+textC
                        num=int(textNum)
                        if(num>a):
                                break
                        if(num==a):
                                respostas.append((b,c))
        return(respostas)

def faz(limit,pot):
        tempoRecorde=0
        for t in range(limit):
                inicio=time()
                num=pos(t,pot)
                if(num):
                        print(str(t)+' : '+str(t**pot))
                        for resp in num:
                                print(str(resp[0])+','+str(resp[1]))
                        print('')
                fim=time()
                duracao=fim-inicio
                if(duracao>=tempoRecorde):
                        print(str(t)+' :'+embelezeTempo(duracao))
                        tempoRecorde=duracao
                        resto=limit-t
                        print('falta :'+embelezeTempo(duracao*resto))
                
faz(10000,2)
