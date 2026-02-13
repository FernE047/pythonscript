from random import sample
from time import time

def tentativaFalha():
    for participante in range(51):
        if(participante not in sample(range(participante,100),50)):
            return(True)
    return(False)


def main() -> None:
    total=0
    comeco=time()
    try:
        while(tentativaFalha()):
            total+=1
    except:
        fim=time()
        duracao=fim-comeco
        print(f"total : {total}")
        print(f"execução total : {duracao}")
        print(f"media total :    {duracao / total}")
        print(f"100k :    {(duracao * 100000) / total}")
        total=input()
    # media 100k : 0.00045391589059292357 segundos


if __name__ == "__main__":
    main()