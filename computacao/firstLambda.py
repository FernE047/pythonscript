def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None, saida: str | None = None
) -> int|str:
    while True:
        entrada = input(f"{mensagem} : ")
        if saida is not None and entrada == saida:
            return saida
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

def polinomio(coefiecientes,x):
    total=len(coefiecientes)
    y=0
    for n,coeficiente in enumerate(coeficientes):
        y+=coeficiente*x**(total-n-1)
    return(y)

def equation(coeficientes):
    return lambda x:polinomio(coeficientes,x)

def intervalo(coeficientes,n):
    funcao=equation(coeficientes)
    comecoEfim=int(n/2)
    print("intervalo entre -"+str(comecoEfim)+" e "+str(comecoEfim))
    for m in range(-comecoEfim,comecoEfim):
        print(str(m)+" : "+str(funcao(m)))      

while True:
    potencia=pegaInteiro("digite a maior potencia",saida="exit")
    if(potencia=="exit"):
        break;
    coeficientes=[]
    for a in range(potencia+1):
        texto="digite o coeficiente de x elevado a "+str(potencia-a)
        coeficientes=[pegaInteiro(texto,saida="exit")]+coeficientes
        if(coeficientes[0]=="exit"):
            break;
    if(coeficientes[0]=="exit"):
        break;
    print(coeficientes)
    n=pegaInteiro("digite o tamanho do intervalo",saida="exit")
    if(n=="exit"):
        break;
    intervalo(coeficientes,n)
