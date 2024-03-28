from random import sample
from time import time

def tentativaFalha():
    for participante in range(51):
        if(participante not in sample(range(participante,100),50)):
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
    print('total : '+str(total))
    print('execução total : '+str(duracao))
    print('media total :    '+str((duracao)/total))
    print('100k :    '+str((duracao*100000)/total))
    total=input()
#media 100k : 0.00045391589059292357 segundos

