from typing import Literal, overload


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

@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...


def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text", "number"] = "text"
) -> str | int:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            if mode == "number":
                return int(user_choice)
            else:
                return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")

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
    print(f"\n{numeroTeste} chega a um fim em {len(termos)-1} passos")
    print(" , ".join(["|".join([str(a) for a in i]) for i in termos]))
    print(" , ".join([str(desconverte(i,base)) for i in termos]))

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
                    if(termos[0]==termos[-1]):
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

def converte(num,base):
    if(num<base):
        return([num])
    return converte(int(num/base),base)+[num%base]

def desconverte(lista,base):
    resultado=0
    for n,a in enumerate(reversed(lista)):
        resultado+=a*base**n
    return(resultado)


def main() -> None:
    limite=100
    base=10
    while True:
        quantia=0
        modo=choose_from_options("qual será o modo?",["Tudo","Apenas Estouros","Sem Estouros","Apenas Passos","Final Esperado","Troca Base","Troca Limites","Finalização"],mode="text")
        if(modo=="5"):
            base=pegaInteiro("digite a nova base")
            continue
        if(modo=="6"):
            limite=pegaInteiro("digite o novo limite")
            continue
        if(modo=="7"):
            break
        if(modo=="3"):
            passos=pegaInteiro("quantos passos?")
        else:
            passos=0
        if(modo=="1"):
            passos=choose_from_options("termos?",["sem","com"],mode="text")
        final=pegaInteiro("procurar até quanto?")
        for numeroTeste in range(final+1):
            try:
                termo=converte(numeroTeste,base)
                sucesso,termos=chegaAFim(termo,limite,base)
                imprime(termos,numeroTeste,modo,sucesso,passos)
                numeroTeste+=1
            except:
                print("deu ruim")
                print(numeroTeste)
        print(f"quantidade total {quantia}")


if __name__ == "__main__":
    main()