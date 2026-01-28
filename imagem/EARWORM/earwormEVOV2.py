from typing import Callable
from PIL import Image
import os


def cadaMusicaFaca(func: Callable[[tuple[str, str]], Image.Image]) -> None:
    pastaMusicas = "C:\\pythonscript\\imagem\\EARWORM\\musicas\\"
    pastaSalvar = "C:\\pythonscript\\imagem\\EARWORM\\imagens\\"
    if not os.path.exists(pastaSalvar):
        os.makedirs(pastaSalvar)
    for nomeArquivo in os.listdir(pastaMusicas):
        if nomeArquivo.endswith(".txt"):
            caminhoCompleto = os.path.join(pastaMusicas, nomeArquivo)
            with open(caminhoCompleto, "r", encoding="utf-8") as f:
                musica = f.read()
            imagem = func((nomeArquivo[:-4], musica))
            imagem.save(os.path.join(pastaSalvar, f"{nomeArquivo[:-4]}.png"))


def fazImagem(info):
    _, musica = info
    musicaSeparada = musica.split(" ")
    quantPalavras = len(musicaSeparada)
    print("quantidade de palavras: " + str(quantPalavras) + "\n")
    if quantPalavras:
        imagem = Image.new("RGBA", (quantPalavras, quantPalavras), (0, 0, 0, 255))
        for coordX in range(quantPalavras):
            for coordY in range(quantPalavras):
                if musicaSeparada[coordX] == musicaSeparada[coordY]:
                    imagem.putpixel((coordX, coordY), (255, 0, 0, 255))
        return imagem


cadaMusicaFaca(fazImagem)
