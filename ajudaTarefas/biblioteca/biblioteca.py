import shelve
from typing import Optional, TypedDict, cast


class SistemaData(TypedDict):
    db_quantia: Optional[int]
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
        sistema_shelf.close()
        sistema_shelf = None


def fazer_menu(options: list[str] | list[LivroData]) -> int:
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


def apresenta_categorias() -> None:
    global sistema
    categorias = sistema["categorias"]
    for indice in range(len(categorias)):
        print(str(indice) + "-" + categorias[indice])


def menu() -> None:
    while True:
        escolha = fazer_menu(["consulta", "adicionar livros", "emprestimo", "sistema"])
        if escolha == 1:
            consulta_menu()
        elif escolha == 2:
            while True:
                if not (adicionar_livro()):
                    break
        elif escolha == 3:
            emprestimo()
        elif escolha == 4:
            altera_sistema()
        else:
            break


def livro_por_local(livro_local: list[tuple[int, int]]) -> list[LivroData]:
    livros: list[LivroData] = []
    if livro_local:
        for locais in livro_local:
            BD = shelve.open("./livrosBD/livro_db{0:04d}".format(locais[0]))
            livros.append(BD["livros"][locais[1]])
    return livros


def apresenta_livro(livros: list[LivroData]) -> None:
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


def consulta_menu() -> tuple[list[LivroData], list[tuple[int, int]]] | None:
    global sistema
    db_quantia = sistema.get("db_quantia", None)
    if db_quantia is None:
        print("não há livros para apresentar")
        return None
    while True:
        escolha = fazer_menu(
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
            livro_local = procura("", 0, 0)
            livros = livro_por_local(livro_local)
            apresenta_livro(livros)
            listas = (livros, livro_local)
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
    db_quantia = sistema.get("db_quantia", None)
    if db_quantia is None:
        raise ValueError("db_quantia is not set in sistema")
    lista_livros: list[tuple[int, int]] = []
    for indice in range(db_quantia + 1):
        BD = shelve.open("./livrosBD/livro_db{0:04d}".format(indice))
        livros = BD["livros"]
        for livro_index in range(len(livros)):
            if comparacao == 1:
                if livros[livro_index][coluna] <= value:
                    lista_livros.append((indice, livro_index))
            elif comparacao == 2:
                if livros[livro_index][coluna] == value:
                    lista_livros.append((indice, livro_index))
            elif comparacao == 3:
                if livros[livro_index][coluna] >= value:
                    lista_livros.append((indice, livro_index))
            else:
                if livros[livro_index][coluna] != "":
                    lista_livros.append((indice, livro_index))
    return lista_livros


def consulta(item: int) -> tuple[list[LivroData], list[tuple[int, int]]] | None:
    global sistema
    categorias = sistema["categorias"]
    livro_local: list[tuple[int, int]] = []
    if item == 0:
        print("qual o nome do livro?")
    elif item == 1:
        print("qual a categoria do livro?")
        while True:
            apresenta_categorias()
            print(str(len(categorias)) + "-indefinido")
            try:
                escolha = int(input())
            except ValueError:
                print("\nsomente inteiros\n")
                continue
            if escolha == len(categorias):
                livro_local = procura("indefinido", item)
                break
            elif escolha not in range(len(categorias)):
                print("\nvocê digitou um valor invalido\n")
            else:
                livro_local = procura(categorias[escolha], item)
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
        livro_local = procura(valor, item)
    elif item == 4:
        print("ainda não temos essa opção\n")
        return None
    elif (item == 6) or (item == 5):
        escolha = fazer_menu(["menor", "igual", "maior"])
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
        livro_local = procura(paginas, item, comparacao=escolha)
    livro = livro_por_local(livro_local)
    apresenta_livro(livro)
    return (livro, livro_local)


# adicionar livros


def adicionar_livro() -> bool:
    global sistema
    db_quantia = sistema.get("db_quantia", 0)
    if db_quantia is None:
        db_quantia = 0
    database = shelve.open("./livrosBD/livro_db{0:04d}".format(db_quantia))
    livro_db: list[LivroData] = database.get("livros", [])
    if len(livro_db) >= 10:
        database = shelve.open("./livrosBD/livro_db{0:04d}".format(db_quantia + 1))
        livro_db = []
        db_quantia += 1
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return False
    print("titulo")
    titulo = input()
    print("Categoria:")
    while True:
        apresenta_categorias()
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
    esse_livro = (titulo, categoria, autor, editora, sinopse, ano, paginas, local)
    livro_db.append(esse_livro)
    database["livros"] = livro_db
    database.close()
    sistema["db_quantia"] = db_quantia
    close_sistema()
    sistema = open_sistema()
    print("adicionar outro?s/n")
    tecla = input()
    return tecla == "s"


# emprestimo


def emprestimo() -> None:
    livro_lugar = consulta_menu()
    if not livro_lugar:
        return
    livro_mudar = fazer_menu(livro_lugar[0])
    if not livro_mudar:
        return
    endereco = livro_lugar[1][livro_mudar - 1]
    muda(endereco, 7)


# referente ao sistema


def altera_sistema() -> None:
    while True:
        escolha = fazer_menu(
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
        categoria_nome = input()
        if categoria_nome == "0":
            break
        categorias.append(categoria_nome)
    sistema["categorias"] = categorias
    close_sistema()
    sistema = open_sistema()
    return


def altera_livro() -> None:
    livro_lugar = consulta_menu()
    if not livro_lugar:
        return
    livro_mudar = fazer_menu(livro_lugar[0])
    if not livro_mudar:
        return
    endereco = livro_lugar[1][livro_mudar - 1]
    item_index = fazer_menu(
        ["nome", "categoria", "autor", "editora", "sinopse", "ano", "paginas", "local"]
    )
    if not item_index:
        return
    muda(endereco, item_index - 1)


def muda(endereco: tuple[int, int], item_index: int) -> None:
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
    BD = shelve.open("./livrosBD/livro_db{0:04d}".format(endereco[0]))
    livros = BD["livros"]
    novo_livro = livros[endereco[1]]
    apresenta_livro([novo_livro])
    print("\n digite " + mudancas[item_index] + " alterado:")
    valor: int | str = 0
    if item_index in [0, 2, 3, 4, 7]:
        valor = input()
    elif item_index == 1:
        while True:
            apresenta_categorias()
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
    elif item_index == 5:
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
    elif item_index == 6:
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
    novo_livro[item_index] = valor
    livros[endereco[1]] = novo_livro
    BD["livros"] = livros
    BD.close()


def altera_categoria() -> None:
    global sistema
    categorias = sistema.get("categorias", [])
    if not categorias:
        print("\nnão há categorias para apresentar\n")
        return
    while True:
        escolha = fazer_menu(categorias)
        if not escolha:
            sistema["categorias"] = categorias
            close_sistema()
            sistema = open_sistema()
            return
        print("escreva o novo nome")
        novo_nome = input()
        velho_nome = categorias[escolha - 1]
        categorias[int(escolha - 1)] = novo_nome
        substituir_categoria(velho_nome, novo_nome)


def substituir_categoria(velho_nome: str, novo_nome: str) -> None:
    global sistema
    db_quantia = sistema["db_quantia"]
    if db_quantia is None:
        raise ValueError("db_quantia is not set in sistema")
    for indice in range(db_quantia + 1):
        BD = shelve.open("./livrosBD/livro_db{0:04d}".format(indice))
        livros = BD["livros"]
        for livro in range(len(livros)):
            if livros[livro][1] == velho_nome:
                livros[livro][1] = novo_nome
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
        escolha = fazer_menu(categorias)
        if not escolha:
            return
        else:
            velho_nome = categorias[escolha - 1]
            del categorias[escolha - 1]
            substituir_categoria(velho_nome, "indefinido")
            sistema["categorias"] = categorias
            print(sistema["categorias"])
            close_sistema()
            sistema = open_sistema()


def retira_livro() -> None:
    livro_lugar = consulta_menu()
    if not livro_lugar:
        return
    livro_mudar = fazer_menu(livro_lugar[0])
    if not livro_mudar:
        return
    endereco = livro_lugar[1][livro_mudar - 1]
    BD = shelve.open("./livrosBD/livro_db{0:04d}".format(endereco[0]))
    livros = BD["livros"]
    del livros[endereco[1]]
    BD["livros"] = livros
    BD.close()


sistema = open_sistema()
menu()
close_sistema()
