import random


def main() -> None:
    soma = 0
    total = 100001
    porcentagem = 0
    probIndividual = [0 for a in range(100)]
    canaisOrigem = [a for a in range(100)]
    random.shuffle(canaisOrigem)
    for jogo in range(total):
        canais = [a for a in canaisOrigem]
        for participante in range(100):
            ehCerto = False
            memoria = []
            for tentativa in range(50):
                chute = random.randint(0, len(canais) - 1)
                while chute in memoria:
                    chute = random.randint(0, len(canais) - 1)
                memoria.append(chute)
                if canais[chute] == participante:
                    ehCerto = True
                    canais.pop(chute)
                    break
            if not (ehCerto):
                probIndividual[participante] += 1
                break
        if ehCerto:
            soma += 1
            print("temos um ganhador")
        porcentagemAtual = int(jogo * 100 / total)
        if porcentagemAtual != porcentagem:
            porcentagem = porcentagemAtual
            print(f"{porcentagem}%")
    for participante, prob in enumerate(probIndividual):
        if prob != 0:
            print(f"participante {participante} : {prob * 100 / total}%")
    print(f"total : {soma * 100 / total}%")


if __name__ == "__main__":
    main()