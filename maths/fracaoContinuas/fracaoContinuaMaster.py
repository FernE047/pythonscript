from typing import Literal, overload

def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


def listaDeInteiros() -> list[int]:
    lista: list[int] = []
    print("digite os inteiros da fração continua um por vez")
    print("quando terminar, digite uma linha vazia")
    while True:
        entrada = input("inteiro: ")
        if entrada == "":
            break
        try:
            valor = int(entrada)
            lista.append(valor)
        except Exception as _:
            print("valor inválido, tente novamente")
    return lista


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...


def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text", "number"] = "text"
) -> str | int:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            if mode == "number":
                return int(user_choice)
            else:
                return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def pegaFloat(mensagem: str) -> float:
    while True:
        entrada = input(mensagem)
        try:
            return float(entrada)
        except Exception as _:
            print("valor inválido, tente novamente")

def fractionToNumber(fraction):
    quant=len(fraction)
    a=fraction[-1]
    print(a)
    print()
    for n in range(quant-1):
        print(quant-n-2)
        print(fraction[quant-n-2])
        a=fraction[quant-n-2]+1/a
        print(a)
        print()
    return a

def decimalToFraction(numero):
    iteracao=0
    fraction=[]
    while True:
        iteracao+=1
        #print()
        inteiro=int(numero)
        #print("inteiro : "+str(inteiro))
        real=numero-inteiro
        #print("real : "+str(real))
        fraction.append(inteiro)
        if(real==0):
            return(fraction)
        else:
            numero=1/real
            #print("invertido : "+str(numero))
        if(iteracao==1000):
            fraction.append(real)
            return(fraction)
        
def fracaoToFraction(numerador,denominador):
    iteracao=0
    fraction=[]
    while True:
        iteracao+=1
        #print()
        inteiro=int(numerador/denominador)
        #print("inteiro : "+str(inteiro))
        velhoNumerador=numerador
        numerador=denominador
        #print("numerador : "+str(numerador))
        denominador=velhoNumerador-inteiro*denominador
        #print("denominador : "+str(denominador))
        fraction.append(inteiro)
        if(denominador==0):
            return(fraction)
        if(numerador==1):
            fraction.append(denominador)
            return(fraction)
        if(iteracao==1000):
            fraction.append(numerador/denominador)
            return(fraction)
        
while True:
    modo=choose_from_options("modo de conversão:",["fração continua para numero","numero para fração continua"],mode="number")
    if(modo):
        modo=choose_from_options("tipo do numero",["decimal","fração","raizes quadradas"],mode="number")
        if(modo==0):
            valor=pegaFloat("digite um valor decimal")
            resultado=decimalToFraction(valor)
        elif(modo==1):
            numerador=pegaInteiro("digite o numerador")
            denominador=pegaInteiro("digite o denominador")
            resultado=fracaoToFraction(numerador,denominador)
        elif(modo==2):
            modo=choose_from_options("modo de raiz:",["simples","complexo"],mode="number") + 2
            raizes=pegaFloat("digite o numero dentro da raiz")
            if(modo==3):
                numerador=pegaInteiro("digite o numero que somará a raiz")
                denominador=pegaInteiro("digite o denominador")
    else:
        fraction=listaDeInteiros()
        resultado=fractionToNumber(fraction)
    print(resultado)
