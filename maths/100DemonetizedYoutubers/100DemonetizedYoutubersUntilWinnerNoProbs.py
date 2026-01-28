from numpy.random import shuffle
from time import time

def tentativaFalha():
    lista=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    shuffle(lista)
    for participante in range(50):
        if(lista.pop(lista.index(participante))<50):
            return(True)
    return(False)

total=0
comeco=time()
try:
    while(tentativaFalha()):
        total+=1
except:
    fim=time()
    duracao=fim-comeco
    print("total : "+str(total))
    print("execução total : "+str(duracao))
    print("media total :    "+str((duracao)/total))
    print("100k :    "+str((duracao*100000)/total))
    print("final :    "+str((duracao*345484498)/total))
    a=input()
fim=time()
duracao=fim-comeco
print("total : "+str(total))
print("execução total : "+str(duracao))
print("media total :    "+str((duracao)/total))
print("100k :    "+str((duracao*100000)/total))
print("final :    "+str((duracao*345484498)/total))
a=input()

#media 100k :       0.00045348677564376093 segundos
#Nova media 100k :  0.0003801782075167559 segundos
#media Numpy 100k : 0.000021456736708393844 segundos

#quantia necessaria: 345484498 no total ou
#quantia necessaria: 1267650600228229401496703205376 no total
