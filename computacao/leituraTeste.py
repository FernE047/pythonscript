# first time reading and writing files in python


def main() -> None:
    with open("vazio.txt", "r", encoding="utf-8") as file:
        print(file)
        lines = file.readlines()
    for line in lines:
        print(line)
    with open("escritaTeste.txt", "w", encoding="utf-8") as file:
        file.write("hello world")
        file.write("\n")


if __name__ == "__main__":
    main()
