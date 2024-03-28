import os

def lePython(nome,lista):
    try:
        file = open(nome,'r')
        linha = file.readline()
        while linha:
            indiceImp = linha.find('import')
            if indiceImp != -1:
                indiceFr = linha.find('from ')
                if indiceFr != -1:
                    linha = linha[indiceFr+5:indiceImp-1]
                else:
                    linha = linha[indice+7:]
                    indice = linha.find(' as ')
                    if indice != -1:
                        linha = linha[:indice]
                if linha not in lista:
                    print(nome)
                    print(linha,end='')
                    print()
                    lista.append(linha)
            linha = file.readline()
        file.close()
    except:
        pass

def anotherVersion(nome):
    try:
        file = open(nome,'r')
        linha = file.readline()
        if linha.find('#v') != -1 :
            return linha
        file.close()
    except:
        try:
            file.close()
        except:
            pass
        pass
    return False

def naoFaz(nome):
    try:
        file = open(nome,'r')
        linha = file.readline()
        if linha.find('#NoBatch') != -1 :
            return True
        file.close()
    except:
        try:
            file.close()
        except:
            pass
        pass
    return False

def fazBat(pastas):
    #print('pastas')
    #print(pastas)
    nomeBat = 'C:\\pythonscript\\'+pastas[-1][:-3]+'.bat'
    print(nomeBat)
    nomePy = '\\'.join(pastas)
    if not naoFaz(nomePy):
        primeiraLinha = anotherVersion(nomePy)
        if primeiraLinha :
            python = 'C:\\Users\\Programador\\AppData\\Local\\Programs\\Python\\Python'+primeiraLinha[2:-1]+'\\python'
        else:
            python = 'python'
        file = open(nomeBat,'w')
        file.write('@echo off\n'+python+' '+nomePy+' %*')#\npause')
        file.close()

def anda(file, nome=None, pastas=None, limite = None):
    lista = LISTA
    if nome:
        #print(nome)
        arquivos = os.listdir(nome)
    else:
        arquivos = os.listdir('C:\\pythonscript')
    arquivosClean = []
    for arquivo in arquivos:
        if arquivo.find('.bat') == -1:
            arquivosClean.append(arquivo)
    arquivos = arquivosClean
    arquivosClean = None
    if not pastas:
        pastas = ['C:','pythonscript']
    if(len(arquivos)>100):
        return None
    if limite:
        if len(pastas)>limite:
            return None
    for arquivo in arquivos:
        if arquivo.find('.') == -1:
            file.write(len(pastas)*'\t'+arquivo+'\n')
            pastas.append(arquivo)
            anda ( file , nome = '\\'.join(pastas) , pastas = pastas , limite = limite)
            pastas.pop(-1)
        else:
            if arquivo.find('txt') != -1:
                file.write(len(pastas)*'\t'+arquivo+'\n')
            if arquivo[-3:] == '.py' :
                file.write(len(pastas)*'\t'+arquivo+'\n')
                #lePython('\\'.join(pastas+[arquivo]),lista)
                pastas.append(arquivo)
                fazBat(pastas)
                pastas.pop(-1)

def criaIndice(nome,limite = None):
    print(nome)
    file = open(nome,'w')
    anda(file,limite = limite)
    file.close()

LISTA = []
criaIndice('superIndice.txt')
criaIndice('indice.txt',limite = 1)
