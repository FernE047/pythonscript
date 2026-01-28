from PIL import Image
import os
from pastaImagens import pegaAssunto as pA

print("digite um assunto")
assunto = input()
imagens = pA(assunto)
for indice, imagem_a in enumerate(imagens):
    print(f"{indice}  -  {imagem_a}")
print("\nqual imagem? 0 a " + str(len(imagens)))
numImagem = int(input())
img = imagens[numImagem]
imagem = Image.open(img)
largura, altura = imagem.size
paleta = []
for x in range(largura):
    for y in range(altura):
        pixel = imagem.getpixel((x, y))
        if pixel not in paleta:
            paleta.append(pixel)
print(paleta)
altura = int(len(paleta) / 256) + 1
if altura > 1:
    paletaImg = Image.new("RGBA", (256, altura), (0, 0, 0, 0))
else:
    paletaImg = Image.new("RGBA", (len(paleta), altura), (0, 0, 0, 0))
m = 0
for index in range(len(paleta)):
    if m % 256 == 0:
        m = 0
    paletaImg.putpixel((m, int(index / 256)), paleta[index])
    m += 1
print(img)
print("digite o novo nome")
nome = input()
paletaImg.save(os.path.join("paleta", "paleta" + nome + ".png"))
