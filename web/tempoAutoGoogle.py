import textos

quantia=1
while quantia!=0:
    trying = True
    while trying:
        try:
            print("\nquantos termos a pesquisar?")
            quantia = int(input())
            trying = False
        except:
            print("digite um número")
    if(quantia!=0):
        minimo = quantia*25
        media = quantia*50
        maximo = quantia*75
        print("\nminimo : "+textos.embelezeTempo(minimo))
        print("media : "+textos.embelezeTempo(media))
        print("maximo : "+textos.embelezeTempo(maximo))
