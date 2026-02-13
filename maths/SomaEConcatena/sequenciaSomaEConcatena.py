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

def fazMensagem(numeroTeste,termos):
    print(f"\n{numeroTeste} chega a um fim em {len(termos)-1} passos")
    print(",".join(termos))

def imprime(termos,numeroTeste,modo,sucesso,passos):
    global quantia
    if(sucesso):
        if(modo!="1"):
            if(modo=="3"):
                if(len(termos)-1==passos):
                    fazMensagem(numeroTeste,termos)
                    quantia+=1
            else:
                if(modo=="4"):
                    if(str(numeroTeste)==termos[-1]):
                        fazMensagem(numeroTeste,termos)
                        quantia+=1
                else:
                    fazMensagem(numeroTeste,termos)
                    quantia+=1
    else:
        if(modo=="0"):
            print(f"{numeroTeste} estorou o limite:")
            print(",".join(termos))
            quantia+=1
        elif(modo=="1"):
            if(passos=="1"):
                print(f"{numeroTeste}:")
                print(",".join(termos))
                quantia+=1
            else:
                print(f"{numeroTeste}")
                quantia+=1


def main() -> None:
    limite=100
    quantia=0
    while True:
        print("qual será o modo?")
        print("0 - tudo\n1 - apenas estouros\n2 - sem estouros\n3 - apenas passos\n4 - final esperado\n5 - finalização")
        modo=input()
        if(modo=="5"):
            break
        if(modo=="3"):
            print("quantos passos?")
            passos=int(input())
        else:
            passos=0
        if(modo=="1"):
            print("com termos ou sem? [1/0]")
            passos=input()
        print("procurar até quanto?")
        final=int(input())
        for numeroTeste in range(final+1):
            try:
                termo=str(numeroTeste)
                sucesso,termos=chegaAFim(termo,limite)
                imprime(termos,numeroTeste,modo,sucesso,passos)
                numeroTeste+=1
            except:
                print(f"{numeroTeste}")
        print(f"quantidade total {quantia}")


if __name__ == "__main__":
    main()