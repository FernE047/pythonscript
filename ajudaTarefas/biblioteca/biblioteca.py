import shelve
from typing import Optional, TypedDict, cast


class SystemData(TypedDict):
    db_quantity: Optional[int]
    categories: list[str]


BookData = tuple[str, str, str, str, str, int, int, str]

system_shelf = None


def open_system() -> SystemData:
    global system_shelf
    system_shelf = shelve.open("./system/system")
    return cast(SystemData, system_shelf)


def close_system() -> None:
    global system_shelf
    if system_shelf is not None:
        system_shelf.close()
        system_shelf = None


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


def show_category_list() -> None:
    global system
    categories = system["categories"]
    for index, category in enumerate(categories):
        print(f"{index}-{category}")


def menu() -> None:
    while True:
        user_choice = make_menu(["display books", "add books", "loan", "system"])
        if user_choice == 1:
            display_book_query_menu()
        elif user_choice == 2:
            while True:
                if not (insert_book()):
                    break
        elif user_choice == 3:
            process_loan()
        elif user_choice == 4:
            manage_system()
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


def display_book_query_menu() -> tuple[list[BookData], list[tuple[int, int]]] | None:
    global system
    db_quantity = system.get("db_quantity", None)
    if db_quantity is None:
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
            book_locations = search_books("", 0, 0)
            books = get_books_by_location(book_locations)
            display_books(books)
            book_data_result = (books, book_locations)
        elif (user_choice >= 2) and (user_choice <= 9):
            result = query_books(user_choice - 2)
            if result is None:
                raise ValueError("query returned None")
            book_data_result = result
        return book_data_result


def search_books(
    value: str | int, column: int, comparison_type: int = 2
) -> list[tuple[int, int]]:
    global system
    db_quantity = system.get("db_quantity", None)
    if db_quantity is None:
        raise ValueError("db_quantity is not set in system")
    found_books: list[tuple[int, int]] = []
    for index in range(db_quantity + 1):
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
    return found_books


def query_books(item: int) -> tuple[list[BookData], list[tuple[int, int]]] | None:
    global system
    categories = system["categories"]
    book_locations: list[tuple[int, int]] = []
    if item == 0:
        print("what is the name of the book?")
    elif item == 1:
        print("what is the category of the book?")
        while True:
            show_category_list()
            print(f"{len(categories)}-undefined")
            try:
                user_choice = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if user_choice == len(categories):
                book_locations = search_books("undefined", item)
                break
            elif user_choice not in range(len(categories)):
                print("\nyou entered an invalid value\n")
            else:
                book_locations = search_books(categories[user_choice], item)
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
        book_locations = search_books(value, item)
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
        book_locations = search_books(pages, item, comparison_type=user_choice)
    books = get_books_by_location(book_locations)
    display_books(books)
    return (books, book_locations)


# add book


def insert_book() -> bool:
    global system
    db_quantity = system.get("db_quantity", 0)
    if db_quantity is None:
        db_quantity = 0
    database = shelve.open(f"./books_database/book_db{db_quantity:04d}")
    book_database: list[BookData] = database.get("books", [])
    if len(book_database) >= 10:
        database = shelve.open(f"./books_database/book_db{db_quantity + 1:04d}")
        book_database = []
        db_quantity += 1
    categories = system.get("categories", [])
    if not categories:
        print("\nno categories to display\n")
        return False
    print("title")
    title = input()
    print("Category:")
    while True:
        show_category_list()
        print(str(len(categories)) + "-add category")
        try:
            user_choice = int(input())
        except ValueError:
            print("\nonly integers\n")
            continue
        if user_choice == len(categories):
            add_category()
            categories = system.get("categories", [])
            continue
        if user_choice not in range(len(categories)):
            print("\nyou entered an invalid value\n")
        else:
            break
    category = categories[user_choice]
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
    system["db_quantity"] = db_quantity
    close_system()
    system = open_system()
    print("add another? y/n")
    continue_input = input()
    return continue_input == "y"


# loan


def process_loan() -> None:
    book_location = display_book_query_menu()
    if not book_location:
        return
    book_change = make_menu(book_location[0])
    if not book_change:
        return
    location = book_location[1][book_change - 1]
    update_book_details(location, 7)


# regarding the system


def manage_system() -> None:
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
            add_category()
        elif user_choice == 2:
            update_category()
        elif user_choice == 3:
            remove_category()
        elif user_choice == 4:
            update_book()
        elif user_choice == 5:
            remove_book()
        else:
            return


def add_category() -> None:
    global system
    categories = system.get("categories", [])
    print("type 0 at any time to exit")
    while True:
        print("type the name of the new category")
        category_name = input()
        if category_name == "0":
            break
        categories.append(category_name)
    system["categories"] = categories
    close_system()
    system = open_system()


def update_book() -> None:
    book_location = display_book_query_menu()
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
    update_book_details(location, item_index - 1)


def update_book_details(location: tuple[int, int], item_index: int) -> None:
    global system
    categories = system.get("categories", [])
    if not categories:
        print("\nno categories to display\n")
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
            show_category_list()
            print(f"{len(categories)}-add category")
            try:
                user_choice = int(input())
            except ValueError:
                print("\nonly integers\n")
                continue
            if user_choice == len(categories):
                add_category()
                categories = system["categories"]
                continue
            if user_choice not in range(len(categories)):
                print("\nyou entered an invalid value\n")
            else:
                break
        updated_value = categories[user_choice]
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


def update_category() -> None:
    global system
    categories = system.get("categories", [])
    if not categories:
        print("\nno categories to display\n")
        return
    while True:
        choice = make_menu(categories)
        if not choice:
            system["categories"] = categories
            close_system()
            system = open_system()
            return
        print("write the new name")
        new_name = input()
        old_name = categories[choice - 1]
        categories[int(choice - 1)] = new_name
        substituir_categoria(old_name, new_name)


def substituir_categoria(old_name: str, new_name: str) -> None:
    global system
    db_quantity = system["db_quantity"]
    if db_quantity is None:
        raise ValueError("db_quantity is not set in system")
    for index in range(db_quantity + 1):
        database = shelve.open(f"./books_database/book_db{index:04d}")
        books = database["books"]
        for book in books:
            if book[1] == old_name:
                book[1] = new_name
        database["books"] = books
        database.close()


def remove_category() -> None:
    global system
    categories = system.get("categories", [])
    if not categories:
        print("\nno categories to display\n")
        return
    while True:
        print(categories)
        choice = make_menu(categories)
        if not choice:
            return
        old_name = categories[choice - 1]
        del categories[choice - 1]
        substituir_categoria(old_name, "undefined")
        system["categories"] = categories
        print(system["categories"])
        close_system()
        system = open_system()


def remove_book() -> None:
    book_location = display_book_query_menu()
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


system = open_system()
menu()
close_system()
