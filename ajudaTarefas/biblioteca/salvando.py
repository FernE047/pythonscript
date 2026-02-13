import shelve


def main() -> None:
    with shelve.open("mydata") as shelf_file:
        book = shelf_file["livro"]
        for category in book:
            print(category)


if __name__ == "__main__":
    main()
