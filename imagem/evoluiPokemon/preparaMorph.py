from userUtil import pegaInteiro as pInt
from PIL import Image
from pastaImagens import pegaImagem as pI
import os

def limpaPasta(pasta):
    arquivos = [pasta+'\\'+a for a in os.listdir(pasta)]
    if('C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized' in arquivos):
        arquivos.pop(arquivos.index('C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized'))
    for arquivo in arquivos:
        os.remove(arquivo)

def salvaLayers(nome):
    fundo = False
    indice = pInt("escolha um pokemon entre 0 e 761", minimo = 0, maximo = 761)
    im = Image.open(pI('PokedexSemFundo',indice))
    im.save('C:\\pythonscript\\imagem\\evoluiPokemon\\' + nome + ".png")
    im.close()

print("IREI EXCLUIR !!!!!")
input()
limpaPasta('C:\\pythonscript\\imagem\\evoluiPokemon\\frames')
limpaPasta('C:\\pythonscript\\imagem\\evoluiPokemon\\frames\\resized')
salvaLayers('inicial')
salvaLayers('final')