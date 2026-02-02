with open("vazio.txt", "r", encoding="utf-8") as file:
    print(file)
    linha = file.readline()
    while linha:
        print(linha)
        linha = file.readline()
with open("escritaTeste.txt", "w", encoding="utf-8") as file:
    file.write("hello world")
    file.write("\n")