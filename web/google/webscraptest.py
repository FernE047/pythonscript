#! python3.
import requests, bs4, re

def resultadosQuantia(termo):
    pesquisa=requests.get(f"https://www.google.com.br/search?q={termo}")
    while(pesquisa.status_code != requests.codes.ok):
        pesquisa=requests.get(f"https://www.google.com.br/search?q={termo}") 
    googleSoup = bs4.BeautifulSoup(pesquisa.text,features="html.parser")        #arruma o HTML
    informacao=googleSoup.select("#resultStats")                                #procura a ID resultstats onde fica a informação
    pegaNumero=re.compile(r"\d{1,3}")                                           #cria um regex para retirada dos números dos pontos
    textoMisturado=informacao[0].getText()                                      #cria um texto "aproximadamente x resultados"
    if(textoMisturado):
        numeroTexto=pegaNumero.findall(textoMisturado)                          #aplica regex para captura do numero
        numero=int("".join(numeroTexto))
    else:
        numero=0
    print(numero)
    return(numero)

def encontrarzero(termo,level=0,levelAtual=0):
    possibilidade=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for a in possibilidade:
        termo=list(termo)
        termo.append(a)
        termo=str("".join(termo))
        print(termo)
        if (levelAtual<level):
            levelAtual+=1
            b=encontrarzero(termo,level,levelAtual)
            if(b!=0):
                return(termo)
            else:
                termo=list(termo)
                del termo[(len(termo)-1)]
                termo=("".join(termo))
        elif(int(resultadosQuantia(termo))==0):
            return(termo)
        termo=list(termo)
        del termo[(len(termo)-1)]
        termo=("".join(termo))
    return(0)			

def encontrar(termo):
    level=0
    levelAtual=0
    termoFinal=encontrarzero(termo,level,0)
    while(termoFinal==0):
        level+=1
        termoFinal=encontrarzero(termo,level,0)
    return(termoFinal)



def main() -> None:
    print("digite o termo de pesquisa")
    termoInicial=input()
    #print("digite o modo de operação:\n1:primeiro\n2:porcentagem\n3:menor numero")
    #modo=int(input())
    resultados=encontrar(termoInicial)
    print(f"\n\nresultado:\n{resultados}")


if __name__ == "__main__":
    main()