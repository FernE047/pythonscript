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

def pegaPeriodo(termoA,termoB):
    periodo=""
    for carac in range(len(termoA)):
        if(carac>len(termoB)-1):
            return(periodo)
        if(termoA[carac]==termoB[carac]):
            periodo+=termoA[carac]
        else:
            return(periodo)


def main() -> None:
    while True:
        print("limite")
        limite=int(input())
        print("primeiro termo")
        termo=input()
        sucesso,termos=chegaAFim(termo,limite)
        if(sucesso):
            print(f"termo {termo} chega a fim em {len(termos)-1}")
            print(",".join(termos))
        else:
            print(f"{termo} estorou o limite:")
            print("\n".join(termos))
            print(f"periodo 1: {pegaPeriodo(termos[-1],termos[-3])}")
            print(f"periodo 2: {pegaPeriodo(termos[-2],termos[-4])}")


if __name__ == "__main__":
    main()