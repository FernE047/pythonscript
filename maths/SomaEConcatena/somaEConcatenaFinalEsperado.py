def chegaAFim(termo,limite):
    termos=[termo]
    while(len(termo)<limite):
        termo=proximoTermo(termo)
        if(termo in termos):
            termos.append(termo)
            break
        else:
            termos.append(termo)
    if(len(termo)>=limite):
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
        resultado=[str(numeroTeste)]
    termo="".join(resultado)
    return(termo)

def fazMensagem(numeroTeste,termos):
    print(f"\n{numeroTeste} chega a um fim em {len(termos)-1} passos")
    print(",".join(termos))


def main() -> None:
    limite=100
    while True:
        modo="4"
        numeroTeste=0
        while True:
            try:
                termo=str(numeroTeste)
                sucesso,termos=chegaAFim(termo,limite)
                if(str(numeroTeste)==termos[-1]):
                    print(f"\n{numeroTeste} chega a um fim em {len(termos)-1} passos")
                    print(",".join(termos))
                numeroTeste+=1
            except:
                print(f"{numeroTeste}")


if __name__ == "__main__":
    main()