import shelve


BookData = tuple[str, str, str, str, str, int, int, str]


def make_menu(options: list[str] | list[BookData]) -> int:
    user_choice = -1
    while True:
        print("Choose:")
        for index, item in enumerate(options):
            print(f"{index + 1}-{item}")
        print("0-back\n")
        try:
            user_choice = int(input())
        except ValueError:
            print("\nintegers only\n")
        if user_choice not in range(len(options) + 1):
            print("\nyou entered an invalid value\n")
        else:
            print("\n")
            return user_choice


class System:
    def __init__(self) -> None:
        self.shelf = shelve.open("./system/system")
        self.categories: list[str] = self.shelf.get("categories", [])
        self.db_quantity: int = self.shelf.get("db_quantity", 0)

    def open_shelf(self) -> None:
        self.shelf = shelve.open("./system/system")

    def close_shelf(self) -> None:
        self.shelf.close()

    def reopen_shelf(self) -> None:
        self.close_shelf()
        self.open_shelf()

    def show_category_list(self) -> None:
        categories = self.categories
        for index, category in enumerate(categories):
            print(f"{index}-{category}")

    def add_categories(self) -> None:
        print("type 0 at any time to exit")
        while True:
            print("type the name of the new category")
            category_name = input()
            if category_name == "0":
                break
            self.categories.append(category_name)
        self.reopen_shelf()

    def is_categories_empty(self) -> bool:
        if len(self.categories) == 0:
            print("\nno categories to display\n")
            return True
        return False

    def update_category(self) -> None:
        if self.is_categories_empty():
            return
        while True:
            choice = make_menu(self.categories)
            if not choice:
                self.reopen_shelf()
                return
            print("write the new name")
            new_name = input()
            old_name = self.categories[choice - 1]
            self.categories[int(choice - 1)] = new_name
            replace_category(old_name, new_name, self)

    def remove_category(self) -> None:
        if self.is_categories_empty():
            return
        while True:
            print(self.categories)
            choice = make_menu(self.categories)
            if not choice:
                return
            old_name = self.categories[choice - 1]
            del self.categories[choice - 1]
            replace_category(old_name, "undefined", self)
            print(self.categories)
            self.reopen_shelf()


def menu(system: System) -> None:
    while True:
        user_choice = make_menu(["display books", "add books", "loan", "system"])
        if user_choice == 1:
            display_book_query_menu(system)
        elif user_choice == 2:
            while True:
                if not (insert_book(system)):
                    break
        elif user_choice == 3:
            process_loan(system)
        elif user_choice == 4:
            manage_system_menu(system)
        else:
            break


def get_books_by_location(book_locations: list[tuple[int, int]]) -> list[BookData]:
    books: list[BookData] = []
    if book_locations:
        for locations in book_locations:
            database = shelve.open(f"./books_database/book_db{locations[0]:04d}")
            books.append(database["books"][locations[1]])
            database.close()
    return books


def display_books(books: list[BookData]) -> None:
    if not books:
        print("No books found\n")
    for book in books:
        print(f"Title: {book[0]}")
        print(f"Category: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"Publisher: {book[3]}")
        print(f"Synopsis: {book[4]}")
        print(f"Year: {str(book[5])}")
        print(f"Pages: {str(book[6])}")
        print(f"Location: {book[7]}\n")


# book queries


def display_book_query_menu(
    system: System,
) -> tuple[list[BookData], list[tuple[int, int]]] | None:
    if system.db_quantity == 0:
        print("no books in the database\n")
        return None
    while True:
        user_choice = make_menu(
            [
                "all books",
                "query by name",
                "query by category",
                "query by author",
                "query by publisher",
                "query by keyword",
                "query by year",
                "query by pages",
                "query by location",
            ]
        )
        book_data_result: tuple[list[BookData], list[tuple[int, int]]] = ([], [])
        if user_choice == 1:
            book_locations = search_books("", 0, system, 0)
            books = get_books_by_location(book_locations)
            display_books(books)
            book_data_result = (books, book_locations)
        elif (user_choice >= 2) and (user_choice <= 9):
            result = query_books(user_choice - 2, system)
            if result is None:
                raise ValueError("query returned None")
            book_data_result = result
        return book_data_result


def search_books(
    value: str | int, column: int, system: System, comparison_type: int = 2
) -> list[tuple[int, int]]:
    found_books: list[tuple[int, int]] = []
    for index in range(system.db_quantity + 1):
        database = shelve.open(f"./books_database/book_db{index:04d}")
        books = database["books"]
        for book_index, book in enumerate(books):
            if comparison_type == 1:
                if book[column] <= value:
                    found_books.append((index, book_index))
            elif comparison_type == 2:
                if book[column] == value:
                    found_books.append((index, book_index))
            elif comparison_type == 3:
                if book[column] >= value:
                    found_books.append((index, book_index))
            else:
                if book[column] != "":
                    found_books.append((index, book_index))
        database.close()
    return found_books


def query_books(
    item: int, system: System
) -> tuple[list[BookData], list[tuple[int, int]]] | None:
    book_locations: list[tuple[int, int]] = []
    if item == 0:
        print("what is the name of the book?")
    elif item == 1:
        print("what is the category of the book?")
        while True:
            system.show_category_list()
            print(f"{len(system.categories)}-undefined")
            try:
                user_choice = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if user_choice == len(system.categories):
                book_locations = search_books("undefined", item, system)
                break
            elif user_choice not in range(len(system.categories)):
                print("\nyou entered an invalid value\n")
            else:
                book_locations = search_books(
                    system.categories[user_choice], item, system
                )
                break
    elif item == 2:
        print("what is the author of the book?")
    elif item == 3:
        print("what is the publisher of the book?")
    elif item == 4:
        print("what is a keyword of the book?")
    elif item == 5:
        print("what is the year of the book?")
    elif item == 6:
        print("how many pages does the book have?")
    elif item == 7:
        print("what is the location of the book?")
    if item in [0, 2, 3, 7]:
        value = input()
        book_locations = search_books(value, item, system)
    elif item == 4:
        print("we don't have this option yet\n")
        return None
    elif (item == 6) or (item == 5):
        user_choice = make_menu(["less", "equal", "greater"])
        pages = 0
        while True:
            print("compared to what value?")
            try:
                pages = int(input())
                if pages < 1:
                    print("\nonly positive integers\n")
                    continue
            except ValueError:
                print("\nonly integers\n")
            break
        book_locations = search_books(pages, item, system, comparison_type=user_choice)
    books = get_books_by_location(book_locations)
    display_books(books)
    return (books, book_locations)


# add book


def insert_book(system: System) -> bool:
    database = shelve.open(f"./books_database/book_db{system.db_quantity:04d}")
    book_database: list[BookData] = database.get("books", [])
    if len(book_database) >= 10:
        database = shelve.open(f"./books_database/book_db{system.db_quantity + 1:04d}")
        book_database = []
        system.db_quantity += 1
    if system.is_categories_empty():
        return False
    print("title")
    title = input()
    print("Category:")
    while True:
        system.show_category_list()
        print(f"{len(system.categories)}-add category")
        try:
            user_choice = int(input())
        except ValueError:
            print("\nonly integers\n")
            continue
        if user_choice == len(system.categories):
            system.add_categories()
            continue
        if user_choice not in range(len(system.categories)):
            print("\nyou entered an invalid value\n")
        else:
            break
    category = system.categories[user_choice]
    print("author")
    author_name = input()
    print("publisher")
    publisher = input()
    print("synopsis")
    synopsis = input()
    while True:
        print("year")
        try:
            year = int(input())
        except ValueError:
            print("\nonly integers\n")
            continue
        if (year > 2100) or (year < 1500):
            print("this year does not exist")
            continue
        break
    pages = 0
    while True:
        print("pages")
        try:
            pages = int(input())
        except ValueError:
            print("\nonly integers\n")
        if pages < 0:
            print("\nonly positive integers\n")
        break
    print("location")
    location = input()
    book = (title, category, author_name, publisher, synopsis, year, pages, location)
    book_database.append(book)
    database["books"] = book_database
    database.close()
    system.db_quantity = system.db_quantity
    system.reopen_shelf()
    print("add another? y/n")
    continue_input = input()
    return continue_input == "y"


# loan


def process_loan(system: System) -> None:
    book_location = display_book_query_menu(system)
    if not book_location:
        return
    book_change = make_menu(book_location[0])
    if not book_change:
        return
    location = book_location[1][book_change - 1]
    update_book_details(location, 7, system)


# regarding the system


def manage_system_menu(system: System) -> None:
    while True:
        user_choice = make_menu(
            [
                "add category",
                "change category",
                "remove category",
                "change book",
                "remove book",
            ]
        )
        if user_choice == 1:
            system.add_categories()
        elif user_choice == 2:
            system.update_category()
        elif user_choice == 3:
            system.remove_category()
        elif user_choice == 4:
            update_book(system)
        elif user_choice == 5:
            remove_book(system)
        else:
            return


def update_book(system: System) -> None:
    book_location = display_book_query_menu(system)
    if not book_location:
        return
    book_change = make_menu(book_location[0])
    if not book_change:
        return
    location = book_location[1][book_change - 1]
    item_index = make_menu(
        [
            "name",
            "category",
            "author",
            "publisher",
            "synopsis",
            "year",
            "pages",
            "location",
        ]
    )
    if not item_index:
        return
    update_book_details(location, item_index - 1, system)


def update_book_details(
    location: tuple[int, int], item_index: int, system: System
) -> None:
    if system.is_categories_empty():
        return
    changes = [
        "name",
        "category",
        "author",
        "publisher",
        "synopsis",
        "year",
        "pages",
        "location",
    ]
    database = shelve.open(f"./books_database/book_db{location[0]:04d}")
    books = database["books"]
    novo_book = books[location[1]]
    display_books([novo_book])
    print(f"\n type the changed {changes[item_index]}:")
    updated_value: int | str = 0
    if item_index in [0, 2, 3, 4, 7]:
        updated_value = input()
    elif item_index == 1:
        while True:
            system.show_category_list()
            print(f"{len(system.categories)}-add category")
            try:
                user_choice = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if user_choice == len(system.categories):
                system.add_categories()
                continue
            if user_choice not in range(len(system.categories)):
                print("\nyou entered an invalid value\n")
            else:
                break
        updated_value = system.categories[user_choice]
    elif item_index == 5:
        while True:
            try:
                updated_value = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if (updated_value > 2100) or (updated_value < 1500):
                print("this year does not exist")
                continue
            break
    elif item_index == 6:
        while True:
            try:
                updated_value = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if updated_value < 0:
                print("\nonly positive integers\n")
                continue
            break
    novo_book[item_index] = updated_value
    books[location[1]] = novo_book
    database["books"] = books
    database.close()


def replace_category(old_name: str, new_name: str, system: System) -> None:
    for index in range(system.db_quantity + 1):
        database = shelve.open(f"./books_database/book_db{index:04d}")
        books = database["books"]
        for book in books:
            if book[1] == old_name:
                book[1] = new_name
        database["books"] = books
        database.close()


def remove_book(system: System) -> None:
    book_location = display_book_query_menu(system)
    if not book_location:
        return
    book_change = make_menu(book_location[0])
    if not book_change:
        return
    address = book_location[1][book_change - 1]
    database = shelve.open(f"./books_database/book_db{address[0]:04d}")
    books = database["books"]
    del books[address[1]]
    database["books"] = books
    database.close()


def main() -> None:
    system = System()
    menu(system)
    system.close_shelf()


if __name__ == "__main__":
    main()
