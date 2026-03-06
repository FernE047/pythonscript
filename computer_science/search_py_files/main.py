from pathlib import Path
from typing import Generator

# this script will search for all .py files in the current directory and its subdirectories, and print their paths and the total count of .py files found.


def traverse_directory(directory_path: Path|None = None) -> Generator[Path]:
    if directory_path is None:
        directory_path = Path.cwd()
    try:
        files = list(directory_path.glob("*.py"))
    except PermissionError:
        return
    for folder in files:
        current_path = directory_path / folder
        if not current_path.is_dir():
            yield current_path
            continue
        for file_path in traverse_directory(current_path):
            yield file_path


def main() -> None:
    files: list[Path] = []
    for file_path in traverse_directory():
        if file_path.suffix == ".py":
            files.append(file_path)
            print(file_path)
    print(len(files))


if __name__ == "__main__":
    main()
