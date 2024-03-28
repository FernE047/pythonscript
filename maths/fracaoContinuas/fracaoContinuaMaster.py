import userUtil

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
    modo=userUtil.entradaNaLista("modo de conversão:",("fração continua para numero","numero para fração continua"),retorno="numerico")
    if(modo):
        modo=userUtil.entradaNaLista("tipo do numero",("decimal","fração","raizes quadradas"),retorno="numerico")
        if(modo==0):
            valor=userUtil.pegaFloat("digite um valor decimal")
            resultado=decimalToFraction(valor)
        elif(modo==1):
            numerador=userUtil.pegaInteiro("digite o numerador")
            denominador=userUtil.pegaInteiro("digite o denominador")
            resultado=fracaoToFraction(numerador,denominador)
        elif(modo==2):
            modo=userUtil.entradaNaLista("modo de raiz:",("simples","complexo"),retorno=(2,3))
            raizes=userUtil.pegaFloat("digite o numero dentro da raiz")
            if(modo==3):
                numerador=userUtil.pegaInteiro("digite o numero que somará a raiz")
                denominador=userUtil.pegaInteiro("digite o denominador")
    else:
        fraction=userUtil.listaDeInteiros()
        resultado=fractionToNumber(fraction)
    print(resultado)
