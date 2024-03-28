#t:face, photo, clip-art, line-drawing, animated
#a:tall, square, wide, panoramic
#s:large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP, >12MP, >15MP, >20MP, >40MP, >70MP
#f:jpg, gif, png, bmp, svg, webp, ico
#l:limit of photos download
import textos
import os
while True:
    print("me dê um input e retornarei 100 imagens / 0 para sair")
    nome=input()
    print("algum argumento adicional?")
    argumento=input()
    if(nome):
        os.system('google_images_download.py -o "C:\pythonscript\Imagens\" -k "'+nome+'" '+argumento)
    else:
        break
    print("baixado")
nomeOriginal=os.path.join('C:\\','pythonscript','Imagens',nome)
nomeNovo=os.path.join('C:\\','pythonscript','Imagens',textos.fazNomeArquivo(nome))
os.rename(nomeOriginal,nomeNovo)
