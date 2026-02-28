import os
from typing import Generator

# this script will search for all .py files in the current directory and its subdirectories, and print their paths and the total count of .py files found.


def traverse_directory(directory_path: str = "") -> Generator[str]:
    if directory_path == "":
        directory_path = os.getcwd()
    files = os.listdir(directory_path)
    for folder in files:
        current_path = f"{directory_path}/{folder}"
        if not os.path.isdir(current_path):
            yield current_path
            continue
        for file_path in traverse_directory(current_path):
            yield file_path


def main() -> None:
    files: list[str] = []
    for file_path in traverse_directory():
        if file_path.find(".py") != -1:
            files.append(file_path)
            print(file_path)
    print(len(files))


if __name__ == "__main__":
    main()
