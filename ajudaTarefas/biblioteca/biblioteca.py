import shelve
from typing import Optional, TypedDict, cast


class SistemaData(TypedDict):
    BDquantia: Optional[int]
    categorias: list[str]


LivroData = tuple[str, str, str, str, str, int, int, str]

sistema_shelf = None


def open_sistema() -> SistemaData:
    global sistema_shelf
    sistema_shelf = shelve.open("./sistema/sistema")
    return cast(SistemaData, sistema_shelf)


def close_sistema() -> None:
    global sistema_shelf
    if sistema_shelf is not None:
        close_sistema()


def fazerMenu(options: list[str] | list[LivroData]) -> int:
    escolha = -1
    while True:
        print("escolha:")
        for item in range(len(options)):
            print(str(item + 1) + "-" + str(options[item]))
        print("0-voltar\n")
        try:
            escolha = int(input())
        except ValueError:
            print("\nsomente inteiros\n")
        if escolha not in range(len(options) + 1):
            print("\nvocê digitou um valor invalido\n")
        else:
            print("\n")
            return escolha


def apresentaCategorias() -> None:
    global sistema
    categorias = sistema["categorias"]
    for indice in range(len(categorias)):
        print(str(indice) + "-" + categorias[indice])


def menu() -> None:
    while True:
        escolha = fazerMenu(["consulta", "adicionar livros", "emprestimo", "sistema"])
        if escolha == 1:
            consultaMenu()
        elif escolha == 2:
            while True:
                if not (adicionarLivro()):
                    break
        elif escolha == 3:
            emprestimo()
        elif escolha == 4:
            altera_sistema()
        else:
            break


def livroPorLocal(livroLocal: list[tuple[int, int]]) -> list[LivroData]:
    livros: list[LivroData] = []
    if livroLocal:
        for locais in livroLocal:
            BD = shelve.open("./livrosBD/livrobd{0:04d}".format(locais[0]))
            livros.append(BD["livros"][locais[1]])
    return livros


def apresentaLivro(livros: list[LivroData]) -> None:
    if not livros:
        print("nenhum livro encontrado\n")
    for livro in livros:
        print("titulo:" + livro[0])
        print("categoria:" + livro[1])
        print("autor:" + livro[2])
        print("editora:" + livro[3])
        print("sinopse:" + livro[4])
        print("ano:" + str(livro[5]))
        print("paginas:" + str(livro[6]))
        print("local:" + livro[7])
        print("\n")


# referente a consulta


def consultaMenu() -> tuple[list[LivroData], list[tuple[int, int]]] | None:
    global sistema
    BDquantia = sistema.get("BDquantia", None)
    if BDquantia is None:
        print("não há livros para apresentar")
        return None
    while True:
        escolha = fazerMenu(
            [
                "todos os livros",
                "consulta por nome",
                "consulta por categoria",
                "consulta por autor",
                "consulta por editora",
                "consulta por palavra chave",
                "consulta por ano",
                "consulta por paginas",
                "consulta por local",
            ]
        )
        listas: tuple[list[LivroData], list[tuple[int, int]]] = ([], [])
        if escolha == 1:
            livroLocal = procura("", 0, 0)
            livros = livroPorLocal(livroLocal)
            apresentaLivro(livros)
            listas = (livros, livroLocal)
        elif (escolha >= 2) and (escolha <= 9):
            result = consulta(escolha - 2)
            if result is None:
                raise ValueError("consulta returned None")
            listas = result
        return listas


def procura(
    value: str | int, coluna: int, comparacao: int = 2
) -> list[tuple[int, int]]:
    global sistema
    BDquantia = sistema.get("BDquantia", None)
    if BDquantia is None:
        raise ValueError("BDquantia is not set in sistema")
    listaLivros: list[tuple[int, int]] = []
    for indice in range(BDquantia + 1):
        BD = shelve.open("./livrosBD/livrobd{0:04d}".format(indice))
        livros = BD["livros"]
        for livro_index in range(len(livros)):
            if comparacao == 1:
                if livros[livro_index][coluna] <= value:
                    listaLivros.append((indice, livro_index))
            elif comparacao == 2:
                if livros[livro_index][coluna] == value:
                    listaLivros.append((indice, livro_index))
            elif comparacao == 3:
                if livros[livro_index][coluna] >= value:
                    listaLivros.append((indice, livro_index))
            else:
                if livros[livro_index][coluna] != "":
                    listaLivros.append((indice, livro_index))
    return listaLivros


def consulta(item: int) -> tuple[list[LivroData], list[tuple[int, int]]] | None:
    global sistema
    categorias = sistema["categorias"]
    livroLocal: list[tuple[int, int]] = []
    if item == 0:
        print("qual o nome do livro?")
    elif item == 1:
        print("qual a categoria do livro?")
        while True:
            apresentaCategorias()
            print(str(len(categorias)) + "-indefinido")
            try:
                escolha = int(input())
            except ValueError:
                print("\nsomente inteiros\n")
                continue
            if escolha == len(categorias):
                livroLocal = procura("indefinido", item)
                break
            elif escolha not in range(len(categorias)):
                print("\nvocê digitou um valor invalido\n")
            else:
                livroLocal = procura(categorias[escolha], item)
                break
    elif item == 2:
        print("qual o autor do livro?")
    elif item == 3:
        print("qual o editora do livro?")
    elif item == 4:
        print("uma palavra chave do livro")
    elif item == 5:
        print("de qual ano o livro é?")
    elif item == 6:
        print("quantas paginas o livro tem?")
    elif item == 7:
        print("qual o local do livro?")
    if item in [0, 2, 3, 7]:
        valor = input()
        livroLocal = procura(valor, item)
    elif item == 4:
        print("ainda não temos essa opção\n")
        return None
    elif (item == 6) or (item == 5):
        escolha = fazerMenu(["menor", "igual", "maior"])
        paginas = 0
        while True:
            print("comparado a")
            try:
                paginas = int(input())
                if paginas < 1:
                    print("\nsomente inteiros positivos\n")
                    continue
            except ValueError:
                print("\nsomente inteiros\n")
            break
        livroLocal = procura(paginas, item, comparacao=escolha)
    livro = livroPorLocal(livroLocal)
    apresentaLivro(livro)
    return (livro, livroLocal)


# adicionar livros


def adicionarLivro() -> bool:
    global sistema
    BD_quantia = sistema.get("BDquantia", 0)
    if BD_quantia is None:
        BD_quantia = 0
    database = shelve.open("./livrosBD/livrobd{0:04d}".format(BD_quantia))
    livroBD: list[LivroData] = database.get("livros", [])
    if len(livroBD) >= 10:
        database = shelve.open("./livrosBD/livrobd{0:04d}".format(BD_quantia + 1))
        livroBD = []
        BD_quantia += 1
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return False
    print("titulo")
    titulo = input()
    print("Categoria:")
    while True:
        apresentaCategorias()
        print(str(len(categorias)) + "-adicionar categoria")
        try:
            escolha = int(input())
        except ValueError:
            print("\nsomente inteiros\n")
            continue
        if escolha == len(categorias):
            adicionar_categoria()
            categorias = sistema.get("categorias", [])
            continue
        if escolha not in range(len(categorias)):
            print("\nvocê digitou um valor invalido\n")
        else:
            break
    categoria = categorias[escolha]
    print("autor")
    autor = input()
    print("editora")
    editora = input()
    print("sinopse")
    sinopse = input()
    while True:
        print("ano")
        try:
            ano = int(input())
        except ValueError:
            print("\nsomente inteiros\n")
            continue
        if (ano > 2100) or (ano < 1500):
            print("esse ano não existe")
            continue
        break
    paginas = 0
    while True:
        print("paginas")
        try:
            paginas = int(input())
        except ValueError:
            print("\nsomente inteiros\n")
        if paginas < 0:
            print("\nsomente inteiros positivos\n")
        break
    print("local")
    local = input()
    esseLivro = (titulo, categoria, autor, editora, sinopse, ano, paginas, local)
    livroBD.append(esseLivro)
    database["livros"] = livroBD
    database.close()
    sistema["BDquantia"] = BD_quantia
    close_sistema()
    sistema = open_sistema()
    print("adicionar outro?s/n")
    tecla = input()
    return tecla == "s"


# emprestimo


def emprestimo() -> None:
    livroLugar = consultaMenu()
    if not livroLugar:
        return
    livroMudar = fazerMenu(livroLugar[0])
    if not livroMudar:
        return
    endereco = livroLugar[1][livroMudar - 1]
    muda(endereco, 7)


# referente ao sistema


def altera_sistema() -> None:
    while True:
        escolha = fazerMenu(
            [
                "adicionar categoria",
                "alterar categoria",
                "remover categoria",
                "alterar livro",
                "remover livro",
            ]
        )
        if escolha == 1:
            adicionar_categoria()
        elif escolha == 2:
            altera_categoria()
        elif escolha == 3:
            retira_categoria()
        elif escolha == 4:
            altera_livro()
        elif escolha == 5:
            retira_livro()
        else:
            return


def adicionar_categoria() -> None:
    global sistema
    categorias = sistema.get("categorias", [])
    print("digite 0 qualquer momento para sair")
    while True:
        print("digite o nome da nova categoria")
        nomeCategoria = input()
        if nomeCategoria == "0":
            break
        categorias.append(nomeCategoria)
    sistema["categorias"] = categorias
    close_sistema()
    sistema = open_sistema()
    return


def altera_livro() -> None:
    livroLugar = consultaMenu()
    if not livroLugar:
        return
    livroMudar = fazerMenu(livroLugar[0])
    if not livroMudar:
        return
    endereco = livroLugar[1][livroMudar - 1]
    itemMudar = fazerMenu(
        ["nome", "categoria", "autor", "editora", "sinopse", "ano", "paginas", "local"]
    )
    if not itemMudar:
        return
    muda(endereco, itemMudar - 1)


def muda(endereco: tuple[int, int], itemMudar: int) -> None:
    global sistema
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return
    mudancas = [
        "nome",
        "categoria",
        "autor",
        "editora",
        "sinopse",
        "ano",
        "paginas",
        "local",
    ]
    BD = shelve.open("./livrosBD/livrobd{0:04d}".format(endereco[0]))
    livros = BD["livros"]
    novoLivro = livros[endereco[1]]
    apresentaLivro([novoLivro])
    print("\n digite " + mudancas[itemMudar] + " alterado:")
    valor: int | str = 0
    if itemMudar in [0, 2, 3, 4, 7]:
        valor = input()
    elif itemMudar == 1:
        while True:
            apresentaCategorias()
            print(str(len(categorias)) + "-adicionar categoria")
            try:
                escolha = int(input())
            except ValueError:
                print("\nsomente inteiros\n")
                continue
            if escolha == len(categorias):
                adicionar_categoria()
                categorias = sistema["categorias"]
                continue
            if escolha not in range(len(categorias)):
                print("\nvocê digitou um valor invalido\n")
            else:
                break
        valor = categorias[escolha]
    elif itemMudar == 5:
        while True:
            try:
                valor = int(input())
            except ValueError:
                print("\nsomente inteiros\n")
                continue
            if (valor > 2100) or (valor < 1500):
                print("esse ano não existe")
                continue
            break
    elif itemMudar == 6:
        while True:
            try:
                valor = int(input())
            except ValueError:
                print("\nsomente inteiros\n")
                continue
            if valor < 0:
                print("\nsomente inteiros positivos\n")
                continue
            break
    novoLivro[itemMudar] = valor
    livros[endereco[1]] = novoLivro
    BD["livros"] = livros
    BD.close()


def altera_categoria() -> None:
    global sistema
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return
    while True:
        escolha = fazerMenu(categorias)
        if not escolha:
            sistema["categorias"] = categorias
            close_sistema()
            sistema = open_sistema()
            return
        print("escreva o novo nome")
        novoNome = input()
        velhoNome = categorias[escolha - 1]
        categorias[int(escolha - 1)] = novoNome
        substituirCategoria(velhoNome, novoNome)


def substituirCategoria(velhoNome: str, novoNome: str) -> None:
    global sistema
    BDquantia = sistema["BDquantia"]
    if BDquantia is None:
        raise ValueError("BDquantia is not set in sistema")
    for indice in range(BDquantia + 1):
        BD = shelve.open("./livrosBD/livrobd{0:04d}".format(indice))
        livros = BD["livros"]
        for livro in range(len(livros)):
            if livros[livro][1] == velhoNome:
                livros[livro][1] = novoNome
        BD["livros"] = livros
        BD.close()


def retira_categoria() -> None:
    global sistema
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return
    while True:
        print(categorias)
        escolha = fazerMenu(categorias)
        if not escolha:
            return
        else:
            velhoNome = categorias[escolha - 1]
            del categorias[escolha - 1]
            substituirCategoria(velhoNome, "indefinido")
            sistema["categorias"] = categorias
            print(sistema["categorias"])
            close_sistema()
            sistema = open_sistema()


def retira_livro() -> None:
    livroLugar = consultaMenu()
    if not livroLugar:
        return
    livroMudar = fazerMenu(livroLugar[0])
    if not livroMudar:
        return
    endereco = livroLugar[1][livroMudar - 1]
    BD = shelve.open("./livrosBD/livrobd{0:04d}".format(endereco[0]))
    livros = BD["livros"]
    del livros[endereco[1]]
    BD["livros"] = livros
    BD.close()


sistema = open_sistema()
menu()
close_sistema()
