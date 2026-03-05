# cria um programa python
import os
from pathlib import Path
import subprocess
from time import time

arquivosQuantia = len(os.listdir())
if arquivosQuantia < 10:
    nomeClone = Path(f"clone{int(time() * 100)}.py")
    original = Path("original.py")
    with open(nomeClone, "w") as clone, open(original, "r") as original_file:
        linha = original_file.readline()
        while linha:
            clone.write(linha)
            linha = original_file.readline()
    subprocess.call(f"python {nomeClone}")
