import os

def walkTree(diretorio=""):
    if diretorio == "":
        diretorio = os.getcwd()
    files = os.listdir(diretorio)
    for folder in files:
        if os.path.isdir(diretorio+"/"+folder):
            for arquivo in walkTree(diretorio+"/"+folder):
                yield arquivo
        else:
            yield diretorio+"/"+folder


def main() -> None:
    files = []
    for arquivo in walkTree():
        if arquivo.find(".py")!= -1:
            files.append(arquivo)
            print(arquivo)
    print(len(files))


if __name__ == "__main__":
    main()