import shelve


def main() -> None:
    shelf_file = shelve.open("mydata")
    book = shelf_file["livro"]
    for category in book:
        print(category)
    shelf_file.close()


if __name__ == "__main__":
    main()
