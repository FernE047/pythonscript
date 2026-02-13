import shelve

from PIL import Image
from numpy.random import shuffle

#    3
#   333
#   3 3
# 22   00
# 22  X  00
# 22   00
#   1 1
#   111
#    1


def minimoEMaximo(lista, horizontal):
    if horizontal:
        quarto = 0
    else:
        quarto = 1
    pos = 0
    menor = 0
    maior = 0
    for a in range(quarto, len(lista), 2):
        if a % 2:
            b = a - 1
        else:
            b = a
        if b % 4 == 0:
            pos += lista[a]
        else:
            pos -= lista[a]
        if pos < menor:
            menor = pos
        if pos > maior:
            maior = pos
    return (menor, maior)



def main() -> None:
    preto = (0, 0, 0, 255)
    branco = (255, 255, 255, 255)
    vermelho = (255, 0, 0, 255)
    minimo = 2
    while True:
        try:
            print("digite o passo maximo da imagem")
            maximo = int(input())
            break
        except:
            print("digite um numero")
    with shelve.open("./numero") as BD:
        imagemNome = BD["imagemNome"]
        bracos = [a for a in range(minimo, maximo + 1)]
        shuffle(bracos)
        print(bracos)
        largura = minimoEMaximo(bracos, True)
        altura = minimoEMaximo(bracos, False)
        inicial = (-largura[0], -altura[0])
        largura = largura[1] - largura[0] + 1
        altura = altura[1] - altura[0] + 1
        print(altura)
        print(largura)
        imagemNova = Image.new("RGBA", (largura, altura), branco)
        print(f"altura :  {altura}")
        print(f"largura : {largura}")
        print(f"inicial : {inicial}")
        imagemNova.putpixel(inicial, vermelho)
        posicao = list(inicial)
        for n, elemento in enumerate(bracos):
            direcao = n % 4
            if direcao == 0:
                for a in range(elemento):
                    posicao[0] += 1
                    imagemNova.putpixel(tuple(posicao), preto)
            elif direcao == 1:
                for a in range(elemento):
                    posicao[1] += 1
                    imagemNova.putpixel(tuple(posicao), preto)
            elif direcao == 2:
                for a in range(elemento):
                    posicao[0] -= 1
                    imagemNova.putpixel(tuple(posicao), preto)
            else:
                for a in range(elemento):
                    posicao[1] -= 1
                    imagemNova.putpixel(tuple(posicao), preto)
        imagemNova.save(f"./imagem{imagemNome}.png")
        imagemNome += 1
        BD["imagemNome"] = imagemNome


if __name__ == "__main__":
    main()