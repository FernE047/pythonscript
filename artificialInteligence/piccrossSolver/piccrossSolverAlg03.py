from time import time
from textos import embelezeTempo
from PIL import Image


def espaco(dica):
    return len(dica) + sum(dica) - 1


def certezasVerticais(jogo):
    for x, dica in enumerate(jogo[1][0]):
        altura = len(jogo[0])
        espacoAtual = espaco(dica)
        espacoSobra = altura - espacoAtual
        if espacoSobra == altura:
            for y in range(0, altura):
                jogo[0][y][x] = -1
        elif espacoSobra == 0:
            y = -2
            for numero in dica:
                y += 2
                if y != 0:
                    jogo[0][y - 1][x] = -1
                for y in range(y, y + numero):
                    jogo[0][y][x] = 1
        elif espacoSobra < max(dica):
            for n, numero in enumerate(dica):
                if espacoSobra < numero:
                    if n == 0:
                        finalY = numero - 1
                    else:
                        finalY = espaco(dica[n:])
                    if n == len(dica) - 1:
                        inicialY = altura - numero
                    else:
                        inicialY = espaco(dica[: n + 1])
                    for y in range(inicialY, finalY):
                        jogo[0][y][x] = 1


def certezasHorizontais(jogo):
    for y, dica in enumerate(jogo[1][1]):
        largura = len(jogo[0][0])
        espacoAtual = espaco(dica)
        espacoSobra = largura - espacoAtual
        if espacoSobra == largura:
            for x in range(0, largura):
                jogo[0][y][x] = -1
        elif espacoSobra == 0:
            x = -2
            for numero in dica:
                if x != -2:
                    jogo[0][y][x + 1] = -1
                for x in range(x + 2, x + 2 + numero):
                    jogo[0][y][x] = 1
        elif espacoSobra < max(dica):
            for n, numero in enumerate(dica):
                if espacoSobra < numero:
                    if n == 0:
                        finalX = numero - 1
                    else:
                        finalX = espaco(dica[n:])
                    if n == len(dica) - 1:
                        inicialX = largura - numero
                    else:
                        inicialX = espaco(dica[: n + 1])
                    for x in range(inicialX, finalX):
                        jogo[0][y][x] = 1


def resolveTabuleiro(jogo):
    certezasHorizontais(jogo)
    certezasVerticais(jogo)


def salva(tabuleiro, nome):
    imagem = Image.new(
        "RGBA", (len(tabuleiro[0]), len(tabuleiro)), (255, 255, 255, 255)
    )
    for y, coluna in enumerate(tabuleiro):
        for x, celula in enumerate(coluna):
            if celula == 1:
                imagem.putpixel((x, y), (0, 0, 0, 255))
    imagem.save(nome + ".png")
    imagem.close()


def resolveUmTabuleiro(jogo):
    print()
    inicio = time()
    solucao = resolveTabuleiro(jogo)
    fim = time()
    tempo = fim - inicio
    global tempoTotal
    tempoTotal += tempo
    completos = 0
    total = 0
    for linha in tabuleiro:
        print()
        for element in linha:
            total += 1
            completos += 1
            if element == 1:
                print("#", end="")
            else:
                if element == 0:
                    print("?", end="")
                    completos -= 1
                else:
                    print("0", end="")
    print("\n\nPorcentagem : " + str(100 * completos / total) + "%")
    print("\n" + embelezeTempo(tempo) + "\n")


nome = "piccross//A{0:03d}"
tempoTotal = 0
for a in range(9):
    picFile = open(nome.format(a) + ".txt")
    config = picFile.read()
    picFile.close()
    horizontalConfig, verticalConfig = config.split("#")
    horizontal = [
        [int(n) for n in dica.split()] for dica in horizontalConfig[:-1].split("\n")
    ]
    vertical = [
        [int(n) for n in dica.split()] for dica in verticalConfig[1:].split("\n")
    ]
    horizontalConfig, verticalConfig, config = [None, None, None]
    tabuleiro = []
    for _ in vertical:
        tabuleiro.append([0 for _ in horizontal]) 
    dicas = [horizontal, vertical]
    jogo = [tabuleiro, dicas]
    resolveUmTabuleiro(jogo)
    print("\n" + embelezeTempo(tempoTotal) + "\n")
    salva(tabuleiro, f"piccross//B{a:03d}")
