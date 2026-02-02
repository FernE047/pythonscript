import os

diretorio = os.getcwd()
imagens = [os.path.join(diretorio, imagem) for imagem in os.listdir()]
with open(os.path.join(diretorio, "copia.py"), "wb", encoding="utf-8") as novoArquivo:
    with open(imagens[0], "rb", encoding="utf-8") as arquivo:
        novoArquivo.write(arquivo.read())
    with open(imagens[0], "rb", encoding="utf-8") as arquivo:
        byte = arquivo.read(1)
        while byte:
            b = novoArquivo.write(byte)
            a = int.from_bytes(byte, byteorder="big")
            a = bin(a)
            a = a.lstrip("0b")
            while len(a) < 8:
                a = "0" + a
            print(a)
            byte = arquivo.read(1)
