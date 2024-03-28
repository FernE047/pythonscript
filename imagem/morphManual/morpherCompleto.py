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
    
inicioDef = time()
#fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\preparaMorph.py ','limpar directory')
#fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\analisaEFazConfig.py ','fazer configurações')
#fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\recolor.py ','recolor')
#fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\morpher.py ','fazer animações')
fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\corrigeFrames.py ','correção de frames')
fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\addBackground.py ','fazer backgrounds')
fazProcesso('python C:\\pythonscript\\imagem\\morphManual\\fazGif.py ','fazer Gif')
fimDef = time()
print('\nfinalizado')
print('execução : '+embelezeTempo(fimDef-inicioDef))
gc.collect()
