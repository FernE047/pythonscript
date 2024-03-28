import imageio
import os
from PIL import Image

def colocaImagemNoGif(writer,nome):
    imagem = imageio.imread(nome)
    writer.append_data(imagem)

factor =4
directory = 'C:\\pythonscript\\imagem\\evoluiPokemon\\'
frames = [directory + 'frames\\'+a for a in os.listdir(directory + 'frames')]
frames.remove(directory + 'frames\\resized')
for nome in frames:
    imagem = Image.open(nome)
    nome = nome[:43]+'\\resized'+nome[43:-4]+'_resize'+nome[-4:]
    imagem.resize(tuple([imagem.size[0]*4,imagem.size[1]*4]),resample = Image.NEAREST).save(nome)
    imagem.close()
nomeGif = directory + 'Animation{0:03d}.gif'.format(len(os.listdir()))
with imageio.get_writer(nomeGif, mode='I') as writer:
    frames = [directory + 'frames\\resized\\'+a for a in os.listdir(directory + 'frames\\resized\\')]
    nome = frames.pop(0)
    for a in range(10):
        colocaImagemNoGif(writer,nome)
    ultimoNome = frames.pop(-1)
    for frame in frames:
        colocaImagemNoGif(writer,frame)
    for a in range(10):
        colocaImagemNoGif(writer,ultimoNome)
print("fim")
