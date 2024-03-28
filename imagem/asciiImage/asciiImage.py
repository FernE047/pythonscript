from PIL import Image
from pastaImagens import pegaAssunto as pA

print("digite um assunto")
assunto=input()
print("quantia")
quantia=input()
if(quantia==''):
    imagens=pA(assunto)
else:
    quantia=int(quantia)
    imagens=pA(assunto,quantia)
niveis=[' ','`','.',',','+','%','@','#']
print('tamanho')
print('165 - max')
print('075 - min')
print('060 - terminal')
print('026 - whats')
tamanho=input()
if(tamanho=='whats'):
    showLargura=26
elif(tamanho=='max'):
    showLargura=165
elif(tamanho=='min'):
    showLargura=75
elif(tamanho=='terminal'):
    showLargura=60
else:
    showLargura=int(tamanho)
for imagem in imagens:
    print('\n'+imagem+'\n')
    imagemColor=Image.open(imagem)
    imagemBW=imagemColor.convert('L')
    largura,altura=imagemBW.size
    if (largura>showLargura):
        aspectRatio=showLargura/largura
        showAltura=int(altura*aspectRatio)
        imagemShow=imagemBW.resize((showLargura,showAltura))
    else:
        imagemShow=imagemBW
    largura,altura=imagemShow.size
    for y in range(altura):
        linha=''
        for x in range(largura):
            pixel=imagemShow.getpixel((x,y))
            linha+=niveis[int(pixel/32)-1]
        print(linha)
    tamanho=input()
