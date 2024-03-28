import textos

def fazLinha(nome):
    inputFile=open(nome+".txt",'r')
    texto=inputFile.read()
    inputFile.close()
    outputFile=open(nome+"NoTabs.txt",'w')
    outputFile.write('<')
    for a in range(1,len(list(texto))):
        caracter=texto[a]
        if(caracter=='<'):
            caracter='\n<'
        outputFile.write(caracter)
    outputFile.close()  

def fazTabulacao(nome,ident,tabs=False):
    if(tabs):
        add=".txt"
    else:
        add="NoTabs.txt"
    inputFile=open(nome+add,'r')
    texto=inputFile.readlines()
    inputFile.close()
    outputFile=open(nome+"Final.txt",'w')
    level=-1
    if ident=="0":
        ident="\t"
    else:
        ident=" "
    for a in range(len(texto)):
        linha=texto[a]
        tagFim=linha.find('>')
        if(linha[tagFim-1]!="/"):
            if(linha[1]!="/"):
                level+=1
                linha=level*ident+linha+"\n"
            else:
                linha=level*ident+linha+"\n"
                level+=-1
            outputFile.write(linha)
    outputFile.close()

escolha="1"
while(escolha!="0"):
    print("\n1 - não tenho nada")
    print("2 - não tem identação")
    print("0 - sair")
    escolha=input()
    if(escolha!="0"):
        print('nome do arquivo (obs: sem ".txt")')
        nome=input()
        print('caracter para identação')
        print('0 - tab')
        print('1 - espaço')
        ident=input()
    if(escolha=="1"):
        fazLinha(nome)
        fazTabulacao(nome,ident)
    elif(escolha=="2"):
        fazTabulacao(nome,ident)
