import shelve

shelf_file = shelve.open("mydata")
book = shelf_file["livro"]
for category in book:
    print(category)
shelf_file.close()
