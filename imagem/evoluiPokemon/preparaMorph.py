from PIL import Image
from pastaImagens import pegaImagem as pI
import os


def pegaInteiro(
    mensagem: str, minimo: int | None = None, maximo: int | None = None
) -> int:
    while True:
        entrada = input(f"{mensagem} : ")
        try:
            valor = int(entrada)
            if (minimo is not None) and (valor < minimo):
                print(f"valor deve ser maior ou igual a {minimo}")
                continue
            if (maximo is not None) and (valor > maximo):
                print(f"valor deve ser menor ou igual a {maximo}")
                continue
            return valor
        except Exception as _:
            print("valor inválido, tente novamente")


def limpaPasta(pasta):
    arquivos = [pasta + "\\" + a for a in os.listdir(pasta)]
    if "C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized" in arquivos:
        arquivos.pop(
            arquivos.index("C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized")
        )
    for arquivo in arquivos:
        os.remove(arquivo)


def salvaLayers(nome):
    fundo = False
    indice = pegaInteiro("escolha um pokemon entre 0 e 761", minimo=0, maximo=761)
    im = Image.open(pI("PokedexSemFundo", indice))
    im.save("C:\\pythonscript\\imagem\\evoluiPokemon\\" + nome + ".png")
    im.close()



def main() -> None:
    print("IREI EXCLUIR !!!!!")
    input()
    limpaPasta("C:\\pythonscript\\imagem\\evoluiPokemon\\frames")
    limpaPasta("C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized")
    salvaLayers("inicial")
    salvaLayers("final")


if __name__ == "__main__":
    main()