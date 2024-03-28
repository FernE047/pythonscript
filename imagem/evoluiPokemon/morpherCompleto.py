import subprocess
import gc
from textos import embelezeTempo
from time import time

#esse algoritmo faz o morph completo

def fazProcesso(processo,nome):
    inicio = time()
    subprocess.call (processo)
    fim = time()
    duracao = fim-inicio
    print(nome+' demorou : '+embelezeTempo(duracao))

while True:
    inicioDef = time()
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\preparaMorph.py ','limpar directory')
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\analisaEFazConfig.py ','fazer configurações')
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\recolor.py ','recolor')
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\morpher.py ','fazer animações')
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\corrigeFrames.py ','correção de frames')
    fazProcesso('python C:\\pythonscript\\imagem\\evoluiPokemon\\fazGif.py ','fazer Gif')
    fimDef = time()
    print('\nfinalizado')
    print('execução : '+embelezeTempo(fimDef-inicioDef))
    gc.collect()
