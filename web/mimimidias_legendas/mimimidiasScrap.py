import os

def leLetra(arq):
    return(arq.read(1))

def lePalavra(arq):
    palavra=""
    letra=leLetra(arq)
    while(letra not in [" ","\n","\t","""]):
        palavra+=letra
        letra=leLetra(arq)
    return(palavra)

def proximaOcorrencia(arq,ocorrencia):
    palavra=lePalavra(arq)
    while(palavra!=ocorrencia):
        palavra=lePalavra(arq)

def leLinha(arq):
    palavra=""
    letra=leLetra(arq)
    while(letra!="\n"):
        palavra+=letra
        letra=leLetra(arq)
    return(palavra)


def main() -> None:
    titulos=open("mimimidias - Youtube.html","r",encoding="utf8")
    newTitulos=open("mimimidiasLINK.txt","w",encoding="utf8")
    while True:
        try:
            proximaOcorrencia(titulos,"title=")
            proximaOcorrencia(titulos,"href=")
            titulo=""
            letra=leLetra(titulos)
            while((letra)and(letra!=""")):
                titulo+=letra
                letra=leLetra(titulos)
            print(titulo)
            newTitulos.write(f"{titulo}\n")
        except:
            break
    newTitulos.close()
    titulos.close()

if __name__ == "__main__":
    main()