import shelve
shelfFile = shelve.open('mydata')
livro=shelfFile['livro']
for categoria in livro:
    print(categoria)
shelfFile.close()
