import shelve

def fazerMenu(lista):
    escolha=-1
    while True:
        print("escolha:")
        for item in range(len(lista)):
            print(str(item+1)+'-'+str(lista[item]))
        print("0-voltar\n")
        try:
            escolha=int(input())
        except:
            print("\nsomente inteiros\n")
        if(escolha not in range(len(lista)+1)):
            print("\nvocê digitou um valor invalido\n")
        else:
            print("\n")
            return(escolha)

def apresentaCategorias():
    global sistema
    categorias=sistema["categorias"]
    for indice in range(len(categorias)):
        print(str(indice)+"-"+categorias[indice])
    
def menu():
    while True:
        escolha=fazerMenu(["consulta","adicionar livros","emprestimo","sistema"])
        if(escolha==1):
            consultaMenu()
        elif(escolha==2):
            while True:
                if(not(adicionarLivro())):
                    break
        elif(escolha==3):
            emprestimo()
        elif(escolha==4):
            alteraSistema()
        else:
            break

def livroPorLocal(livroLocal):
    livros=[]
    if(livroLocal):
        for locais in livroLocal:
            BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(locais[0]))
            livros.append(BD["livros"][locais[1]])
    return(livros)

def apresentaLivro(livros):
    if not livros:
        print("nenhum livro encontrado\n")
    for livro in livros:
        print("titulo:"+livro[0])
        print("categoria:"+livro[1])
        print("autor:"+livro[2])
        print("editora:"+livro[3])
        print("sinopse:"+livro[4])
        print("ano:"+str(livro[5]))
        print("paginas:"+str(livro[6]))
        print("local:"+livro[7])
        print("\n")
    
    
        
#referente a consulta

def consultaMenu():
    try:
        BDquantia=sistema["BDquantia"]
    except:
        print("não há livros para apresentar")
        return()
    while True:
        escolha=fazerMenu(["todos os livros","consulta por nome","consulta por categoria","consulta por autor","consulta por editora","consulta por palavra chave","consulta por ano","consulta por paginas","consulta por local"])
        if(escolha==1):
            livroLocal=procura("",0,0)
            livros=livroPorLocal(livroLocal)
            apresentaLivro(livros)
            listas=[livros,livroLocal]
        elif(escolha>=2)and(escolha<=9):
            listas=consulta(escolha-2)
        else:
            return(listas)

def procura(valor,coluna,comparacao=2):
    global sistema
    BDquantia=sistema["BDquantia"]
    listaLivros=[]
    for indice in range(BDquantia+1):
        BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(indice))
        livros = BD["livros"]
        for livro in range(len(livros)):
            if(comparacao==1):
                if(livros[livro][coluna]<=valor):
                    listaLivros.append([indice,livro])
            elif(comparacao==2):
                if(livros[livro][coluna]==valor):
                    listaLivros.append([indice,livro])
            elif(comparacao==3):
                if(livros[livro][coluna]>=valor):
                    listaLivros.append([indice,livro])
            else:
                if(livros[livro][coluna]!=""):
                    listaLivros.append([indice,livro])
    return(listaLivros)

def consulta(item):
    global sistema
    BDquantia=sistema["BDquantia"]
    categorias=sistema["categorias"]
    if(item==0):
        print("qual o nome do livro?")
    elif(item==1):
        print("qual a categoria do livro?")
        while True:
            apresentaCategorias()
            print(str(len(categorias))+"-indefinido")
            try:
                escolha=int(input())
            except:
                print("\nsomente inteiros\n")
                continue
            if(escolha==len(categorias)):
                livroLocal=procura("indefinido",item)
                break
            elif(escolha not in range(len(categorias))):
                print("\nvocê digitou um valor invalido\n")
            else:
                livroLocal=procura(categorias[escolha],item)
                break
    elif(item==2):
        print("qual o autor do livro?")
    elif(item==3):
        print("qual o editora do livro?")
    elif(item==4):
        print("uma palavra chave do livro")
    elif(item==5):
        print("de qual ano o livro é?")
    elif(item==6):
        print("quantas paginas o livro tem?")
    elif(item==7):
        print("qual o local do livro?")
    if(item in [0,2,3,7]):
        valor=input()
        livroLocal=procura(valor,item)
    elif(item==4):
        print("ainda não temos essa opção\n")
        return()
    elif((item==6)or(item==5)):
        escolha=fazerMenu(["menor","igual","maior"])
        while True:
            print("comparado a")
            try:
                paginas=int(input())
            except:
                print("\nsomente inteiros\n")
            if(paginas<1):
                print("\nsomente inteiros positivos\n")
            break
        livroLocal=procura(paginas,item,comparacao=escolha)
    livro=livroPorLocal(livroLocal)
    apresentaLivro(livro)
    return([livro,livroLocal])
        
        
#adicionar livros
        
def adicionarLivro():
    global sistema
    try:
        BDquantia=sistema["BDquantia"]
    except:
        BDquantia=0
    BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(BDquantia))
    try:
        livroBD = BD["livros"]
        if len(livroBD)>=10:
            BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(BDquantia+1))
            livroBD = []
            BDquantia+=1
    except:
        livroBD = []
    try:
        categorias=sistema["categorias"]
    except:
        print("\nnão há categorias para apresentar\n")
        return()
    print("titulo")
    titulo=input()
    print("Categoria:")
    while True:
        apresentaCategorias()
        print(str(len(categorias))+"-adicionar categoria")
        try:
            escolha=int(input())
        except:
            print("\nsomente inteiros\n")
            continue
        if(escolha==len(categorias)):
            adicionarCategoria()
            categorias=sistema["categorias"]
            continue
        if(escolha not in range(len(categorias))):
            print("\nvocê digitou um valor invalido\n")
        else:
            break
    categoria=categorias[escolha]
    print("autor")
    autor=input()
    print("editora")
    editora=input()
    print("sinopse")
    sinopse=input()
    while True:
        print("ano")
        try:
            ano=int(input())
        except:
            print("\nsomente inteiros\n")
            continue
        if((ano>2100)or(ano<1500)):
            print("esse ano não existe")
            continue
        break
    while True:
        print("paginas")
        try:
            paginas=int(input())
        except:
            print("\nsomente inteiros\n")
        if(paginas<0):
            print("\nsomente inteiros positivos\n")
        break
    print("local")
    local=input()
    esseLivro=[titulo,categoria,autor,editora,sinopse,ano,paginas,local]
    livroBD.append(esseLivro)
    BD["livros"]=livroBD
    BD.close()
    sistema["BDquantia"]=BDquantia
    sistema.close
    sistema=shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/sistema/sistema')
    print("adicionar outro?s/n")
    tecla=input()
    if(tecla=="s"):
        return(True)
    else:
        return(False)
    
    
#emprestimo
    
def emprestimo():
    livroLugar=consultaMenu()
    if not livroLugar:
        return()
    livroMudar=fazerMenu(livroLugar[0])
    if not livroMudar:
        return()
    endereco=livroLugar[1][livroMudar-1]
    muda(endereco,7)

#referente ao sistema

def alteraSistema():
    while True:
        escolha=fazerMenu(["adicionar categoria","alterar categoria","remover categoria","alterar livro","remover livro"])
        if(escolha==1):
            adicionarCategoria()
        elif(escolha==2):
            alteraCategoria()
        elif(escolha==3):
            retiraCategoria()
        elif(escolha==4):
            alteraLivro()
        elif(escolha==5):
            retiraLivro()
        else:
            break
    return()

def adicionarCategoria():
    global sistema
    try:
        categorias=sistema["categorias"]
    except:
        categorias=[]
    print("digite 0 qualquer momento para sair")
    while True:
        print("digite o nome da nova categoria")
        nomeCategoria=input()
        if(nomeCategoria=="0"):
            break
        categorias.append(nomeCategoria)
    sistema["categorias"]=categorias
    sistema.close()
    sistema=shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/sistema/sistema')
    return()

def alteraLivro():
    livroLugar=consultaMenu()
    if not livroLugar:
        return()
    livroMudar=fazerMenu(livroLugar[0])
    if not livroMudar:
        return()
    endereco=livroLugar[1][livroMudar-1]
    itemMudar=fazerMenu(["nome","categoria","autor","editora","sinopse","ano","paginas","local"])
    if not itemMudar:
        return()
    muda(endereco,itemMudar-1)

def muda(endereco,itemMudar):
    global sistema
    try:
        categorias=sistema["categorias"]
    except:
        print("\nnão há categorias para apresentar\n")
        return()
    mudancas=["nome","categoria","autor","editora","sinopse","ano","paginas","local"]
    BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(endereco[0]))
    livros=BD["livros"]
    novoLivro=livros[endereco[1]]
    apresentaLivro([novoLivro])
    print("\n digite "+mudancas[itemMudar]+" alterado:")
    if(itemMudar in [0,2,3,4,7]):
        valor=input()
        novoLivro[itemMudar]=valor
    elif(itemMudar==1):
        while True:
            apresentaCategorias()
            print(str(len(categorias))+"-adicionar categoria")
            try:
                escolha=int(input())
            except:
                print("\nsomente inteiros\n")
                continue
            if(escolha==len(categorias)):
                adicionarCategoria()
                categorias=sistema["categorias"]
                continue
            if(escolha not in range(len(categorias))):
                print("\nvocê digitou um valor invalido\n")
            else:
                break
        valor=categorias[escolha]
    elif(itemMudar==5):
        while True:
            try:
                valor=int(input())
            except:
                print("\nsomente inteiros\n")
                continue
            if((valor>2100)or(valor<1500)):
                print("esse ano não existe")
                continue
            break
    elif(itemMudar==6):
        while True:
            try:
               valor=int(input())
            except:
                print("\nsomente inteiros\n")
            if(valor<0):
                print("\nsomente inteiros positivos\n")
            break
    novoLivro[itemMudar]=valor
    livros[endereco[1]]=novoLivro
    BD["livros"]=livros
    BD.close()    
    
def alteraCategoria():
    global sistema
    try:
        categorias=sistema["categorias"]
    except:
        print("\nnão há categorias para apresentar\n")
        return()
    while True:
        escolha=fazerMenu(categorias)
        if not escolha:
            break
        else:
            print("escreva o novo nome")
            novoNome=input()
            velhoNome=categorias[escolha-1]
            categorias[int(escolha-1)]=novoNome
            substituirCategoria(velhoNome,novoNome)
    sistema["categorias"]=categorias
    sistema.close()
    sistema=shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/sistema/sistema')

def substituirCategoria(velhoNome,novoNome):
    global sistema
    BDquantia=sistema["BDquantia"]
    for indice in range(BDquantia+1):
        BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(indice))
        livros = BD["livros"]
        for livro in range(len(livros)):
            if(livros[livro][1]==velhoNome):
                livros[livro][1]=novoNome
        BD["livros"] = livros
        BD.close()
    return()

def retiraCategoria():
    global sistema
    try:
        categorias=sistema["categorias"]
    except:
        print("\nnão há categorias para apresentar\n")
        return()
    while True:
        print(categorias)
        escolha=fazerMenu(categorias)
        if not escolha:
            return()
        else:
            velhoNome=categorias[escolha-1]
            del categorias[escolha-1]
            substituirCategoria(velhoNome,"indefinido")
            sistema["categorias"]=categorias
            print(sistema["categorias"])
            sistema.close()
            sistema=shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/sistema/sistema')

def retiraLivro():
    livroLugar=consultaMenu()
    if not livroLugar:
        return()
    livroMudar=fazerMenu(livroLugar[0])
    if not livroMudar:
        return()
    endereco=livroLugar[1][livroMudar-1]
    BD = shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/livrosBD/livrobd{0:04d}'.format(endereco[0]))
    livros=BD["livros"]
    del livros[endereco[1]]
    BD["livros"]=livros
    BD.close()    

sistema=shelve.open('C:/pythonscript/ajudaTarefas/biblioteca/sistema/sistema')
menu()
