from time import time
from PIL import Image


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)


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


def situacaoCompara(situacoes, dica, ultimaCelula, limite, tamanho):
    if dica[0] == 0:
        if situacoes:
            return False
        else:
            return True
    if len(situacoes) > len(dica):
        return False
    if situacoes:
        if len(situacoes) > 1:
            for index, situacao in enumerate(situacoes[:-1]):
                if situacao != dica[index]:
                    return False
        else:
            index = -1
        if ultimaCelula != 1:
            if situacoes[index + 1] != dica[index + 1]:
                return False
            if len(situacoes) < len(dica):
                if (
                    tamanho - (limite + 1)
                    < len(dica[len(situacoes) :]) + sum(dica[len(situacoes) :]) - 1
                ):
                    return False
        else:
            if situacoes[index + 1] > dica[index + 1]:
                return False
            if situacoes[index + 1] == dica[index + 1]:
                if (
                    tamanho - (limite + 1)
                    < len(dica[len(situacoes) :]) + sum(dica[len(situacoes) :]) - 2
                ):
                    return False
            else:
                if (
                    tamanho - (limite + 1)
                    < len(dica[len(situacoes) :])
                    + sum(dica[len(situacoes) :])
                    + dica[index + 1]
                    - situacoes[index + 1]
                    - 1
                ):
                    return False
    else:
        if tamanho - (limite + 1) < len(dica) + sum(dica) - 1:
            return False
    return True


def verificaColunasParcial(tabuleiro, dicas, limiteY, minimoX, limiteX, novaLinha):
    for x in range(minimoX, limiteX):
        dica = dicas[0][x]
        situacao = []
        ultimaCelula = 0
        for y in range(limiteY + 1):
            if y == limiteY:
                if novaLinha:
                    celula = novaLinha[x - minimoX]
                else:
                    celula = tabuleiro[y][x]
            else:
                celula = tabuleiro[y][x]
            if ultimaCelula == 1:
                if celula == 1:
                    contagem += 1
                else:
                    situacao.append(contagem)
            else:
                if celula == 1:
                    contagem = 1
            ultimaCelula = celula
        if ultimaCelula == 1:
            situacao.append(contagem)
        if not situacaoCompara(situacao, dica, ultimaCelula, limiteY, len(tabuleiro)):
            return False
    return True


def possibilidades(tamanho, dica, dicas, tabuleiro, y):
    if not (dica):
        return [[-1 for a in range(tamanho)]]
    if tamanho == dica[0]:
        return [[1 for a in range(tamanho)]]
    if dica[0] == 0:
        return [[-1 for a in range(tamanho)]]
    if len(dica) - 1 + sum(dica) == tamanho:
        possibilidade = []
        for n in dica:
            for a in range(n):
                possibilidade.append(1)
            possibilidade.append(-1)
        possibilidade.pop(-1)
        return [possibilidade]
    lista = []
    numero = dica[0]
    if len(dica) == 1:
        for inicial in range(tamanho - numero + 1):
            possibilidade = [-1 for a in range(tamanho)]
            for x in range(numero):
                possibilidade[inicial + x] = 1
            if verificaColunasParcial(
                tabuleiro,
                dicas,
                y,
                len(dicas[0]) - tamanho,
                len(dicas[0]) - tamanho + len(possibilidade),
                possibilidade,
            ):
                lista.append(possibilidade)
    else:
        for inicial in range(tamanho - numero + 1 - sum(dica[1:]) - len(dica[1:])):
            possibilidade = [-1 for a in range(inicial + numero)]
            for x in range(numero):
                possibilidade[inicial + x] = 1
            if verificaColunasParcial(
                tabuleiro,
                dicas,
                y,
                len(dicas[0]) - tamanho,
                len(dicas[0]) - tamanho + len(possibilidade) + 1,
                possibilidade + [-1],
            ):
                adicionais = possibilidades(
                    tamanho - inicial - numero - 1, dica[1:], dicas, tabuleiro, y
                )
                for add in adicionais:
                    lista.append(possibilidade + [-1] + add)
    return lista


def resolveTabuleiro(tabuleiro, dicas, numeroLinha):
    if numeroLinha == len(tabuleiro):
        return tabuleiro
    else:
        linhaOriginal = tabuleiro[numeroLinha]
        for linhaPoss in possibilidades(
            len(tabuleiro[0]), dicas[1][numeroLinha], dicas, tabuleiro, numeroLinha
        ):
            global tries
            tries += 1
            tabuleiro[numeroLinha] = linhaPoss
            solucao = resolveTabuleiro(tabuleiro, dicas, numeroLinha + 1)
            if solucao:
                return solucao
        tabuleiro[numeroLinha] = linhaOriginal


def resolveUmTabuleiro(tabuleiro, dicas):
    print()
    global tries
    tries = 0
    cortes = 0
    inicio = time()
    solucao = resolveTabuleiro(tabuleiro, dicas, 0)
    fim = time()
    print("\ntentativas: " + str(tries))
    tempo = fim - inicio
    global tempoTotal
    tempoTotal += tempo
    for linha in tabuleiro:
        print()
        for element in linha:
            if element > 0:
                print("#", end="")
            else:
                if element == 0:
                    print("?", end="")
                else:
                    print("0", end="")
    print()
    print("\n" + embelezeTempo(tempo) + "\n")


# nome = pS("qual o nome do arquivo?")
nome = "piccross//A{0:03d}"
tempoTotal = 0
for index in range(8):
    picFile = open(nome.format(index) + ".txt")
    config = picFile.read()
    picFile.close()
    horizontal, vertical = config.split("#")
    horizontal = [
        [int(n) for n in dica.split()] for dica in horizontal[:-1].split("\n")
    ]
    vertical = [[int(n) for n in dica.split()] for dica in vertical[1:].split("\n")]
    tabuleiro = []
    for _ in vertical:
        tabuleiro.append([0 for _ in horizontal])
    dicas = [horizontal, vertical]
    resolveUmTabuleiro(tabuleiro, dicas)
    print("\n" + embelezeTempo(tempoTotal) + "\n")
    salva(tabuleiro, nome.format(index))
print("\n" + embelezeTempo(tempoTotal) + "\n\n\n")
