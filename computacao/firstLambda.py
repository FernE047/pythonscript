from userUtil import pegaInteiro

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

validaInt=lambda texto:pegaInteiro(texto,saida="exit")
while True:
    potencia=validaInt("digite a maior potencia")
    if(potencia=="exit"):
        break;
    coeficientes=[]
    for a in range(potencia+1):
        texto="digite o coeficiente de x elevado a "+str(potencia-a)
        coeficientes=[validaInt(texto)]+coeficientes
        if(coeficientes[0]=="exit"):
            break;
    if(coeficientes[0]=="exit"):
        break;
    print(coeficientes)
    n=validaInt("digite o tamanho do intervalo")
    if(n=="exit"):
        break;
    intervalo(coeficientes,n)
