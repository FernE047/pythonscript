# cria um programa python
import os
import subprocess
from time import time

arquivosQuantia = len(os.listdir())
if arquivosQuantia < 10:
    nomeClone = f"clone{int(time() * 100)}.py"
    with open(nomeClone, "w") as clone, open("original.py", "r") as original:
        linha = original.readline()
        while linha:
            clone.write(linha)
            linha = original.readline()
    subprocess.call(f"python {nomeClone}")
