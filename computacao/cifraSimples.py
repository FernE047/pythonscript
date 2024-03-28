from string import ascii_uppercase
from string import ascii_lowercase
from userUtil import pegaString

def trocaLetra(letra,n):
    n%=26
    if(letra in ascii_lowercase):
        letrinhas=list(ascii_lowercase)
        indice=(n+letrinhas.index(letra))%26
        letra=letrinhas[indice]
    elif(letra in ascii_uppercase):
        letronas=list(ascii_uppercase)
        indice=(n+letronas.index(letra))%26
        letra=letronas[indice]
    return(letra)

def cifra(texto, n):
    novoTexto=""
    for a in list(texto):
        novoTexto+=trocaLetra(a,n)
    return(novoTexto)

def todasCifras(texto):
    print(texto,end="\n\n")
    for n in range(1,26):
        print("{:02d}:".format(n))
        print(cifra(texto,n),end="\n\n")
            
texto=pegaString("digite alguma coisa e cifraremos")
todasCifras(texto)
