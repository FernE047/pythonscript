def chegaAFim(termo,limite):
    termos=[termo]
    while(len(termo)<limite):
        termo=proximoTermo(termo)
        if(termo in termos):
            termos.append(termo)
            break
        else:
            termos.append(termo)
    if(len(termo)>limite):
        return([False,termos])
    else:
        return([True,termos])

def proximoTermo(termo):
    resultado=[]
    if(len(termo)<=1):
        return(termo)
    for indice in range(len(termo)-1):
        digito1=termo[indice]
        digito2=termo[indice+1]
        soma=int(digito1)+int(digito2)
        bidigito=str(soma)
        resultado.append(bidigito)
    if(not(resultado)):
        resultado=[termo]
    termo="".join(resultado)
    return(termo)

while True:
    print("limite")
    limite=int(input())
    #limite=165
    print("primeiro termo")
    termo=input()
    sucesso,termos=chegaAFim(termo,limite)
    if(sucesso):
        print("termo "+termo+" chega a fim em "+str(len(termos)-1))
        print(",".join(termos))
    else:
        print(termo+" estorou o limite:")
        print("\n".join(termos))
