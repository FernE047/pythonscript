from send2trash import send2trash
import userUtil
import random
import textos
import os

#simple system to register answers and questions
#the user can create categories and modules
#each module has a question and answer file
#the user can study the modules in random order

def imprimeModulo(nome):
    fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'r')
    filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'r')
    linhaResposta = fileRespostas.readline()
    linhaPergunta = filePerguntas.readline()
    indice = 1
    while linhaResposta:
        print(indice,end=') \n')
        print(linhaPergunta,end='')
        print(linhaResposta+'\n')
        linhaResposta = fileRespostas.readline()
        linhaPergunta = filePerguntas.readline()
        indice += 1
    fileRespostas.close()
    filePerguntas.close()
    
def editarModulo(pasta,modulo):
    opcoes = ['Voltar']
    opcoes += ['Adicionar']
    opcoes += ['Alterar']
    opcoes += ['Remover']
    escolha = userUtil.entradaNaLista('escolha uma opcao : ',opcoes)
    if escolha in ['Alterar','Remover'] :
        imprimeModulo(pasta + '\\' + modulo)
        quantia = quantiaLinhas('\\'.join([pasta,modulo,'answer.txt']))
        indiceAltera = userUtil.pegaInteiro("digite o indice que deseja alterar",minimo = 1,maximo = quantia)
        fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'r')
        filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'r')
        fileRespostasTemp = open('\\'.join([pasta,modulo,'answer.txt.tmp']),'w')
        filePerguntasTemp = open('\\'.join([pasta,modulo,'question.txt.tmp']),'w')
        linhaResposta = fileRespostas.readline()
        linhaPergunta = filePerguntas.readline()
        indice = 1
        while linhaResposta:
            if indice == indiceAltera:
                if escolha == 'Alterar':
                    palavra = userUtil.pegaString('digite a palavra pergunta')
                    filePerguntasTemp.write(palavra+'\n')
                    palavra = userUtil.pegaString('digite a palavra resposta')
                    fileRespostasTemp.write(palavra+'\n')
            else:
                fileRespostasTemp.write(linhaResposta)
                filePerguntasTemp.write(linhaPergunta)
                print(indice,end=') \n')
                print(linhaPergunta,end='')
                print(linhaResposta+'\n')
            linhaResposta = fileRespostas.readline()
            linhaPergunta = filePerguntas.readline()
            indice += 1
        fileRespostas.close()
        filePerguntas.close()
        fileRespostasTemp.close()
        filePerguntasTemp.close()
        send2trash('\\'.join([pasta,modulo,'answer.txt']))
        send2trash('\\'.join([pasta,modulo,'question.txt']))
        os.rename('\\'.join([pasta,modulo,'answer.txt.tmp']),'\\'.join([pasta,modulo,'answer.txt']))
        os.rename('\\'.join([pasta,modulo,'question.txt.tmp']),'\\'.join([pasta,modulo,'question.txt']))
    if escolha == 'Adicionar':
        imprimeModulo(pasta + '\\' + modulo)
        fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'a')
        filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'a')
        while True:
            palavra = userUtil.pegaString('digite a palavra pergunta')
            if palavra == '0':
                break
            filePerguntas.write(palavra+'\n')
            palavra = userUtil.pegaString('digite a palavra resposta')
            fileRespostas.write(palavra+'\n')
        fileRespostas.close()
        filePerguntas.close()

def excluirModulo(pasta,modulo):
    send2trash('\\'.join([pasta,modulo]))
    print("Removido Modulo " + modulo)

def fazPergunta(fileA,fileB,indice,escolha):
    if escolha == 'Respostas':
        fileC = fileB
        fileB = fileA
        fileA = fileC
        fileC = None
    else:
        modo = random.randint(0,1)
        if modo:
            fileC = fileB
            fileB = fileA
            fileA = fileC
            fileC = None
    linhaA = fileA.readline()
    linhaB = fileB.readline()
    indiceAtual = 0
    while linhaA:
        if indice == indiceAtual:
            resposta = userUtil.pegaString(linhaA[:-1])
            if resposta == '0':
                return resposta
            if resposta == linhaB[:-1]:
                print("\tCERTO!!!\n")
            else:
                print('\terrou\n')
            return resposta
        linhaA = fileA.readline()
        linhaB = fileB.readline()
        indiceAtual += 1

def quantiaLinhas(fileName):
    file = open(fileName,'r')
    linha = file.readline()
    quantia = 0
    while linha:
        quantia += 1
        linha = file.readline()
    file.close()
    return quantia

def acessarModulo(pasta,modulo):
    quantia = quantiaLinhas('\\'.join([pasta,modulo,'answer.txt']))
    opcoes = ['Voltar']
    opcoes += ['Perguntas']
    opcoes += ['Respostas']
    opcoes += ['Perguntas & Respostas']
    escolha = userUtil.entradaNaLista('escolha um modo : ',opcoes)
    print("digite 0 em qualquer lugar para sair")
    
    while True:
        fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'r')
        filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'r')
        indice = random.randint(0,quantia)
        resposta = fazPergunta(filePerguntas,fileRespostas,indice,escolha)
        fileRespostas.close()
        filePerguntas.close()
        if resposta == '0':
            break

def criaModulo(pasta,pastaAv,modulo):
    print(pasta+'\\'+modulo)
    if not os.path.exists(pasta+'\\'+modulo):
        os.makedirs(pasta+'\\'+modulo)
        os.makedirs(pastaAv+'\\'+modulo)
        fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'w')
        filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'w')
        print('digite 0 em uma pergunta para sair ')
        while True:
            palavra = userUtil.pegaString('digite a palavra pergunta')
            if palavra == '0':
                break
            filePerguntas.write(palavra+'\n')
            palavra = userUtil.pegaString('digite a palavra resposta')
            fileRespostas.write(palavra+'\n')
        fileRespostas.close()
        filePerguntas.close()
    else:
        print('já existe')

def modoAleatorio(pasta,modo): #adicionar modular parcial
    modulos = os.listdir(pasta)
    opcoes = ['Voltar']
    opcoes += ['Perguntas']
    opcoes += ['Respostas']
    opcoes += ['Perguntas & Respostas']
    escolha = userUtil.entradaNaLista('escolha um modo : ',opcoes)
    print("digite 0 em qualquer lugar para sair")
    isParcial = True if modo.find('Parcial')!=-1 else False
    if isParcial:
        modo = modo[8:]
        while True:
            opcoes = ['Concluir Seleção']
            indice = userUtil.entradaNaLista('escolha quais modulos retirar : ', opcoes+modulos, retorno = 'numerico')
            if indice == 0:
                break
            if len(modulos) == 1:
                print("não é possivel excluir o último modulo")
                break
            else:
                modulos.pop(indice-1)
    if modo == 'Total':
        quantias = [quantiaLinhas('//'.join([pasta,a,'answer.txt'])) for a in modulos]
    while True:
        if modo =='Total':
            soma = 0
            indice = -1
            linhaRequerida = random.randint(1,sum(quantias))
            while soma < linhaRequerida:
                indice += 1
                soma += quantias[indice]
            modulo = modulos[indice]
        else:
            modulo = modulos[random.randint(0,len(modulos)-1)]
        indice = random.randint(0,quantiaLinhas('//'.join([pasta,modulo,'answer.txt'])))
        fileRespostas = open('\\'.join([pasta,modulo,'answer.txt']),'r')
        filePerguntas = open('\\'.join([pasta,modulo,'question.txt']),'r')
        resposta = fazPergunta(filePerguntas,fileRespostas,indice,escolha)
        fileRespostas.close()
        filePerguntas.close()
        if resposta == '0':
            break
        
while True:
    diretorio = 'C:\\pythonscript\\ajudaTarefas\\quickLearning'
    escolha = userUtil.entradaNaLista('escolha uma categoria : ',['Sair','Criar Nova']+os.listdir(diretorio+'\\categorias'))
    if escolha == "Sair":
        break
    if escolha == "Criar Nova":
        nomeCategoriaNovo = userUtil.pegaString('digite o nome da nova categoria : ')
        pasta = diretorio+'\\categorias\\'+textos.fazNomeArquivo(nomeCategoriaNovo)
        pastaAv =diretorio+'\\avaliacao\\'+textos.fazNomeArquivo(nomeCategoriaNovo)
        print(pasta)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            os.makedirs(pastaAv)
        else:
            print('já existe')
        continue
    else:
        pasta = diretorio+'\\categorias\\'+escolha
        pastaAv = diretorio+'\\avaliacao\\'+escolha
    while True:
        opcoes = ['Voltar']
        opcoes += ['Modulos']
        if len(os.listdir(pasta)) != 0:
            opcoes += ['Aleatorio']
        escolha = userUtil.entradaNaLista('escolha uma opcao : ',opcoes)
        if escolha == "Voltar":
            break
        if escolha == "Modulos":
            while True:
                opcoes = ['Voltar']
                opcoes += ['Novo']
                categorias = os.listdir(pasta)
                escolha = userUtil.entradaNaLista('escolha uma opcao : ',opcoes+categorias)
                if escolha == "Voltar":
                    break
                if escolha == "Novo":
                    modulo = userUtil.pegaString('digite o nome do novo modulo : ')
                    criaModulo(pasta,pastaAv,textos.fazNomeArquivo(modulo))
                else:
                    modulo = escolha
                    opcoes = ['Voltar']
                    opcoes += ['Visualizar']
                    opcoes += ['Estudar']
                    opcoes += ['Editar']
                    opcoes += ['Excluir']
                    escolha = userUtil.entradaNaLista('escolha uma opcao : ',opcoes)
                    if escolha == 'Visualizar':
                        imprimeModulo(pasta+'\\'+modulo)
                    if escolha == 'Editar':
                        editarModulo(pasta,modulo)
                    if escolha == 'Excluir':
                        excluirModulo(pasta,modulo)
                    if escolha == 'Estudar':
                        acessarModulo(pasta,modulo)
        if escolha == "Aleatorio":
            modulos = os.listdir(pasta)
            opcoes = ['Voltar']
            opcoes += ['Total']
            if(len(modulos) > 1):
                opcoes += ['Simples']
                opcoes += ['Parcial Total']
                opcoes += ['Parcial Simples']
            while True:
                escolha = userUtil.entradaNaLista('escolha uma opcao : ',opcoes)
                if escolha == "Voltar":
                    modulos = None
                    break
                else:
                    modoAleatorio(pasta,escolha)
