import os
import subprocess


def hasDotJavaInside(pasta):
    for arquivo in [diretorio + "\\" + arq for arq in os.listdir(pasta)]:
        if arquivo.find(".java") != -1:
            return True
    return False


def fazBat(nome):
    nomeProject = nome[nome.rfind("\\") + 1 : nome.rfind(".")]
    nomeBat = "C:\\JavaProgs\\" + nomeProject + ".bat"
    print(nomeBat)
    nomeJava = pasta + "\\" + nomeProject
    with open(nomeBat, "w",encoding="utf-8") as file:
        file.write("@echo off\njava " + nomeJava + " %*")  # \npause")



def fazBatProject(nome):
    nomeProject = nome[nome.rfind("\\") + 1 :]
    nomeBat = "C:\\JavaProgs\\" + nomeProject + ".bat"
    print(nomeBat)
    nomeJava = pasta + "\\teste.Teste"
    with open(nomeBat, "w",encoding="utf-8") as file:
        file.write("@echo off\njava " + nomeJava + " %*")  # \npause()

diretorio = "C:\\JavaProgs"
for pasta in [diretorio + "\\" + folder for folder in os.listdir(diretorio)]:
    if hasDotJavaInside(pasta):
        print("javac " + pasta + "\\*.java")
        subprocess.Popen("javac " + pasta + "\\*.java", shell=True)
        fazBat(pasta)
    else:
        print("dir /s /B " + pasta + "\\*.java > " + pasta + "\\sources.txt")
        subprocess.Popen(
            "dir /s /B " + pasta + "\\*.java > " + pasta + "\\sources.txt", shell=True
        )
        subprocess.Popen("javac @" + pasta + "\\sources.txt", shell=True)
        fazBatProject(pasta)
