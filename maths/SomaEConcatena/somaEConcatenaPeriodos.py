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
    termo=''.join(resultado)
    return(termo)

def pegaPeriodo(termoA,termoB):
    periodo=''
    for carac in range(len(termoA)):
        if(carac>len(termoB)-1):
            return(periodo)
        if(termoA[carac]==termoB[carac]):
            periodo+=termoA[carac]
        else:
            return(periodo)

while True:
    print('modo:\n\n1 - tudo\n2 - não\n3 - sim')
    modo=input()
    print('limite')
    limite=int(input())
    print('final')
    final=int(input())
    for numeroTeste in range(final+1):
        termo=str(numeroTeste)
        sucesso,termos=chegaAFim(termo,limite)
        if(not(sucesso)):
            periodo1=pegaPeriodo(termos[-1],termos[-3])
            periodo2=pegaPeriodo(termos[-2],termos[-4])
            if((periodo1=='')or(periodo2=='')):
                if(modo!='3'):
                    #print(termo+' não tem periodos')
                    print(termo)
            else:
                if(modo!='2'):
                    print('\n'+termo+' tem periodos:')
                    print('periodo 1:'+periodo1)
                    print('periodo 2:'+periodo2)
            #print('\n'.join(termos))
