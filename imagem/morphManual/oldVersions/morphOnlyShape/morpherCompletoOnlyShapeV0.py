import subprocess
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
fazProcesso('python C:\\pythonscript\\imagem\\morphOnlyShape\\analisaEFazConfig.py ','fazer configurações')
fazProcesso('python C:\\pythonscript\\imagem\\morphOnlyShape\\morpher.py ','fazer animações')
fimDef = time()
print('\nfinalizado')
print('execução : '+embelezeTempo(fimDef-inicioDef))
a = input()
