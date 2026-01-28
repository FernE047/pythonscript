import imageio
import os
from PIL import Image


def colocaImagemNoGif(writer, nome):
    imagem = imageio.imread(nome)
    writer.append_data(imagem)


def resize(nome):
    factor = 4
    imagem = Image.open(nome)
    if imagem.size[0] * imagem.size[1] < 10000:
        nome = nome[:41] + "\\resized" + nome[41:-4] + "_resize" + nome[-4:]
        imagem.resize(
            tuple([imagem.size[0] * 4, imagem.size[1] * 4]), resample=Image.NEAREST
        ).save(nome)
    else:
        imagem.save(nome[:41] + "\\resized" + nome[41:])
    imagem.close()


directory = "C:\\pythonscript\\imagem\\morphManual\\"
frames = [f"{directory}frames\\{a}" for a in os.listdir(f"{directory}frames")]
frames.remove(f"{directory}frames\\resized")
for frame in frames:
    resize(frame)
nomeGif = f"{directory}Animation{len(os.listdir(directory)):03d}.gif"
with imageio.get_writer(nomeGif, mode="I") as writer:
    frames = [
        directory + "frames\\resized\\" + a
        for a in os.listdir(directory + "frames\\resized\\")
    ]
    nome = frames.pop(0)
    for a in range(10):
        colocaImagemNoGif(writer, nome)
    ultimoNome = frames.pop(-1)
    for frame in frames:
        colocaImagemNoGif(writer, frame)
    for a in range(10):
        colocaImagemNoGif(writer, ultimoNome)
print("fim")
