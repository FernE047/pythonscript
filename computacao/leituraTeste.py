# first time reading and writing files in python

with open("vazio.txt", "r", encoding="utf-8") as file:
    print(file)
    line = file.readline()
    while line:
        print(line)
        line = file.readline()
with open("escritaTeste.txt", "w", encoding="utf-8") as file:
    file.write("hello world")
    file.write("\n")