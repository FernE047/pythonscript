import random


def main() -> None:
    minimo=10
    maximo=200
    jogos=1000000
    valores={}
    for a in range(1,maximo+1):
        valores[a]=0
    for rodada in range(jogos):
        numeros=random.randint(minimo,maximo)
        sorteado=random.randint(1,numeros)
        valores[sorteado]+=1
    for numero in valores:
        if(valores[numero]!=0):
            print(f"{numero:03d} : {valores[numero]*100/jogos}%")


if __name__ == "__main__":
    main()