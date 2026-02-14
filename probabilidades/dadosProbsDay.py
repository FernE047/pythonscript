# calcula probabilidade de cair todos os dados o mesmo numero, de 1 a 20 dados
# imprime a quantidade de seculos, anos, dias, horas, minutos, segundos


def main() -> None:
    for a in range(0, 20):
        print(f"\nquantia de dados: {a + 1}")
        vezes = 6**a
        minuto = 0
        hora = 0
        dia = 0
        ano = 0
        seculo = 0
        if vezes > 60:
            minuto = int(vezes / 12)
        else:
            print(f"segundos: {vezes}")
        if minuto >= 1:
            hora = int(minuto / 60)
            minuto = minuto % 60
            print(f"minuto: {minuto}")
        if hora >= 1:
            dia = int(hora / 24)
            hora = hora % 24
            print(f"horas: {hora}")
        if dia >= 1:
            ano = int(dia / 365.25)
            dia = dia % 365
            print(f"dia: {dia}")
        if ano >= 1:
            seculo = int(ano / 100)
            ano = ano % 100
            print(f"ano: {ano}")
        if seculo >= 1:
            print(f"seculo: {seculo}")
        print(f"probabilidade: 1 em {vezes}")


if __name__ == "__main__":
    main()
