from pathlib import Path


def write_lines(file_path: Path) -> None:
    with open(file_path.with_suffix(".txt"), "r") as file:
        text = file.read()
    with open(file_path.with_suffix("NoTabs.txt"), "w") as output_file:
        output_file.write("<")
        for character in list(text)[1:]:
            if character == "<":
                character = "\n<"
            output_file.write(character)


def make_tabulation(name: Path, ident: str, tabs: bool = False) -> None:
    if tabs:
        filename = name.with_suffix(".txt")
    else:
        filename = name.with_suffix("NoTabs.txt")
    with open(filename, "r") as file:
        lines = file.readlines()
    with open(name.with_suffix("Final.txt"), "w") as output_file:
        level = -1
        if ident == "0":
            ident = "\t"
        else:
            ident = " "
        for line in lines:
            end_tag = line.find(">")
            if line[end_tag - 1] == "/":
                continue
            if line[1] != "/":
                level += 1
                line = f"{level * ident}{line}\n"
            else:
                line = f"{level * ident}{line}\n"
                level += -1
            output_file.write(line)


def main() -> None:
    user_choice = "1"
    while user_choice != "0":
        print("\n1 - no lines and no indentation")
        print("2 - no indentation")
        print("0 - exit")
        user_choice = input()
        if user_choice == "0":
            return
        print("file name (without extension)")
        name = Path(input())
        print("character for indentation")
        print("0 - tab")
        print("1 - space")
        ident = input()
        if user_choice == "1":
            write_lines(name)
            make_tabulation(name, ident)
        elif user_choice == "2":
            make_tabulation(name, ident)


if __name__ == "__main__":
    main()
