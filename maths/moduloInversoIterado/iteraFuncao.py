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

def formula(a,b,n):
    if((b==0)and(n==0)):
        return 1
    return a*n+b

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def fatoresPrimos(n):
    if(n<=1):
        return str(n)
    fatores=prime_factors(n)
    ultimo=fatores[0]
    n=0
    retorno=str(ultimo)+"^"
    for a in fatores:
        if(a==ultimo):
            n+=1
        else:
            retorno+=str(n)+"*"+str(a)+"^"
            n=1
        ultimo=a
    retorno+=str(n)
    return retorno

def itera(funcao,inicio=0):
    valor=funcao(inicio)
    for a in range(inicio,24):
        print(str(a)+" : "+str(valor)+" : ",end="")
        print(fatoresPrimos(valor))
        valor=funcao(valor)
    print(str(a+1)+" : "+str(valor)+" : "+fatoresPrimos(valor))


def main() -> None:
    while True:
        base = pegaInteiro("\nescreva base")
        if(base==0):
            break
        resto = pegaInteiro("escreva resto")
        comeco = pegaInteiro("escreva o inicio")
        funcao = lambda x : formula(base,resto,x)
        if(resto==0):
            itera(funcao,inicio=comeco)
        else:
            itera(funcao,inicio=comeco)


if __name__ == "__main__":
    main()