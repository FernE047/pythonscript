# cria um programa python
import os
import subprocess
from time import time

arquivosQuantia = len(os.listdir())
if arquivosQuantia < 10:
    nomeClone = "clone" + str(int(time() * 100)) + ".py"
    clone = open(nomeClone, "w")
    original = open("original.py", "r")
    linha = original.readline()
    while linha:
        clone.write(linha)
        linha = original.readline()
    clone.close()
    subprocess.call("python " + nomeClone)
    original.close()
