import userUtil

def chegaAFim(termo,limite,base):
    termos=[termo]
    while(len(termo)<limite):
        termo=proximoTermo(termo,base)
        if(termo in termos):
            termos.append(termo)
            break
        else:
            termos.append(termo)
    if(len(termo)>limite):
        return([False,termos])
    else:
        return([True,termos])

def proximoTermo(termo,base):
    resultado=[]
    if(len(termo)<=1):
        return(termo)
    for indice in range(len(termo)-1):
        digito1=termo[indice]
        digito2=termo[indice+1]
        soma=digito1+digito2
        if soma>=base:
            bidigito=converte(soma,base)
        else:
            bidigito=[soma]
        resultado+=bidigito
    if(not(resultado)):
        resultado=[]+termo
    return(resultado)

def fazMensagem(numeroTeste,termos):
    global base
    print('\n'+str(numeroTeste)+' chega a um fim em '+str(len(termos)-1)+' passos')
    print(' , '.join(["|".join([str(a) for a in i]) for i in termos]))
    print(' , '.join([str(desconverte(i,base)) for i in termos]))

def imprime(termos,numeroTeste,modo,sucesso,passos):
    global quantia
    if(sucesso):
        if(modo!='1'):
            if(modo=='3'):
                if(len(termos)-1==passos):
                    fazMensagem(numeroTeste,termos)
                    quantia+=1
            else:
                if(modo=='4'):
                    if(termos[0]==termos[-1]):
                        fazMensagem(numeroTeste,termos)
                        quantia+=1
                else:
                    fazMensagem(numeroTeste,termos)
                    quantia+=1
    else:
        if(modo=='0'):
            print(str(numeroTeste)+' estorou o limite:')
            print(','.join(termos))
            quantia+=1
        elif(modo=='1'):
            if(passos=='1'):
                print(str(numeroTeste)+':')
                print(','.join(termos))
                quantia+=1
            else:
                print(str(numeroTeste))
                quantia+=1

def converte(num,base):
    if(num<base):
        return([num])
    return converte(int(num/base),base)+[num%base]

def desconverte(lista,base):
    resultado=0
    for n,a in enumerate(reversed(lista)):
        resultado+=a*base**n
    return(resultado)

limite=100
base=10
while True:
    quantia=0
    modo=userUtil.entradaNaLista("qual será o modo?",["Tudo","Apenas Estouros","Sem Estouros","Apenas Passos","Final Esperado","Troca Base","Troca Limites","Finalização"],retorno="numericoStr")
    if(modo=='5'):
        base=userUtil.pegaInteiro("digite a nova base")
        continue
    if(modo=='6'):
        limite=userUtil.pegaInteiro("digite o novo limite")
        continue
    if(modo=='7'):
        break
    if(modo=='3'):
        passos=userUtil.pegaInteiro("quantos passos?")
    else:
        passos=0
    if(modo=='1'):
        passos=userUtil.entradaNaLista("termos?",["sem","com"],retorno="numericoStr")
    final=userUtil.pegaInteiro("procurar até quanto?")
    for numeroTeste in range(final+1):
        try:
            termo=converte(numeroTeste,base)
            sucesso,termos=chegaAFim(termo,limite,base)
            imprime(termos,numeroTeste,modo,sucesso,passos)
            numeroTeste+=1
        except:
            print("deu ruim")
            print(numeroTeste)
    print('quantidade total '+str(quantia))
