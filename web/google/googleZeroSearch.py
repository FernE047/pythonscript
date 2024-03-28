#! python3.
import requests, bs4, re
import internet
import time

def resultadosQuantia(termo):
    informacao=internet.siteProcura('https://www.google.com.br/search?q='+termo,'#resultStats')                              
    pegaNumero=re.compile(r'\d{1,3}')                                           
    textoMisturado=informacao[0].getText()                                      
    if(textoMisturado):
        numeroTexto=pegaNumero.findall(textoMisturado)                          
        numero=int(''.join(numeroTexto))
    else:
        numero=0
    print(numero)
    return(int(numero))

def encontrarZero(termo):
    proxima=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    contagem=[]
    menor=0
    for letra in proxima:
        contagem.append(0)
    for letra in range(len(proxima)):
        termo=list(termo)
        termo.append(proxima[letra])
        termo=str(''.join(termo))
        print(termo)
        quantidade=resultadosQuantia(termo)
        if(quantidade==0):
            print('\n\n O Termo "'+termo+'" tem 0 resultados')
            return(0)
        else:
            if(quantidade==1):
                sites=internet.resultadosGoogle(termo)
                for site in sites:
                    print(str(site))
            contagem[letra]=quantidade
            if(quantidade<=contagem[menor]):
                menor=letra
        termo=list(termo)
        del termo[(len(termo)-1)]
        termo=(''.join(termo))
    termo=list(termo)
    termo.append(proxima[menor])
    termo=str(''.join(termo))
    return(encontrarZero(termo))

print('digite o termo de pesquisa')
termoInicial=input()
startTime=time.time()
encontrarZero(termoInicial)
endTime=time.time()
realTime=endTime-startTime
print("levou "+str(realTime)+" segundos")


