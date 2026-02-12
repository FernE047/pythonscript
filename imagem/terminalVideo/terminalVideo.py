from PIL import Image
import os

diretorio="./video"

def imagemToText(imagem):
    global showAltura
    global niveis
    global showLargura
    imagemColor=Image.open(imagem)
    imagemBW=imagemColor.convert("L")
    largura,altura=imagemBW.size
    if(showAltura==0):
        if (largura>showLargura):
            aspectRatio=showLargura/largura
            showAltura=int(altura*aspectRatio)
        else:
            showAltura=altura  
    imagemShow=imagemBW.resize((showLargura,showAltura))  
    largura,altura=imagemShow.size
    texto=""
    for y in range(altura):
        linha=""
        for x in range(largura):
            pixel=imagemShow.getpixel((x,y))
            linha+=niveis[int(pixel/32)]
        texto+=linha + "\n"
    return(texto)


def main() -> None:
    showAltura=0
    niveis=[" ","▫","□","O","░","▒","▓","█"]
    showLargura= 60
    imagens=[os.path.join(diretorio,imagem)for imagem in os.listdir(diretorio)]
    for imagem in imagens:
        texto=imagemToText(imagem)
        apaga=len(texto)
        os.system("cls" if os.name == "nt" else "clear")
        print(texto+(apaga*"\b"),end="",flush=True)


if __name__ == "__main__":
    main()