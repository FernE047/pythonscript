#! python3.
def collatz(numero):
    print(str(numero))
    if (numero != 1) and (numero % 2):
        numero = 3 * numero + 1
    elif numero % 2 == 0:
        numero = int(numero / 2)
    else:
        return
    collatz(numero)


while True:
    print("digite um numero:")
    try:
        valor = int(input())
        if valor <= 0:
            print("somente numeros positivos")
            continue
        else:
            collatz(valor)
            break
    except ValueError:
        print("Somente numeros são permitidos")
        continue
