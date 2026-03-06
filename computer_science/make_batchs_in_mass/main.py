from io import TextIOWrapper
from pathlib import Path
from typing import Literal

# I used to have a batch file for each python script to run it directly from terminal.


def read_python(filename: Path, imported_modules: list[str]) -> None:
    def add_imported_modules(line: str) -> None:
        if line in imported_modules:
            return
        print(filename)
        print(line, end="")
        print()
        imported_modules.append(line)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
    except Exception as _:
        return
    for line in lines:
        if not line:
            continue
        import_index = line.find("import")
        if import_index == -1:
            line = file.readline()
            continue
        import_from_index = line.find("from ")
        if import_from_index != -1:
            line = line[import_from_index + 5 : import_index - 1]
            add_imported_modules(line)
            continue
        line = line[import_index + 7 :]
        import_as_index = line.find(" as ")
        if import_as_index != -1:
            line = line[:import_as_index]
        add_imported_modules(line)


def get_python_version(filename: Path) -> str | Literal[False]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            line = file.readline()
            if line.find("#v") != -1:
                return f"C:/Users/Programador/AppData/Local/Programs/Python/Python{line[2:-1]}/python"
    except Exception as _:
        pass
    return "python"


def check_no_batch_flag(filename: Path) -> bool:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            line = file.readline()
            if line.find("#NoBatch") != -1:
                return True
    except Exception as _:
        pass
    return False


def create_batch_file(folders: list[Path]) -> None:
    batch_name = Path("C:") / "pythonscript" / f"{folders[-1].stem}.bat"
    print(batch_name)
    python_filename = folders[0]
    for folder in folders[1:]:
        python_filename /= folder
    if not check_no_batch_flag(python_filename):
        python_exe = get_python_version(python_filename)
        with open(batch_name, "w", encoding="utf-8") as file:
            file.write(f"@echo off\n{python_exe} {python_filename} %*")


def filter_batch_files(file_list: list[Path]) -> list[Path]:
    filtered_files: list[Path] = []
    for file in file_list:
        if file.suffix.lower() != ".bat":
            filtered_files.append(file)
    return filtered_files


def explore_directory(
    output_file: TextIOWrapper,
    current_folder: Path | None = None,
    folder_list: list[Path] | None = None,
    folder_limit: int | None = None,
) -> None:
    if current_folder is not None:
        files = list(current_folder.iterdir())
    else:
        files = list((Path("C:") / "pythonscript").iterdir())
    if folder_list is None:
        folder_list = [Path("C:"), Path("pythonscript")]
    if folder_limit is not None:
        if len(folder_list) > folder_limit:
            return None
    files = filter_batch_files(files)
    if len(files) > 100:
        return None
    for file in files:
        if file.is_dir():
            output_file.write(f"{len(folder_list) * '\t'}{file}\n")
            folder_list.append(file)
            explore_directory(
                output_file,
                current_folder=file,
                folder_list=folder_list,
                folder_limit=folder_limit,
            )
            folder_list.pop()
        else:
            if file.suffix == ".txt":
                output_file.write(f"{len(folder_list) * '\t'}{file}\n")
            if file.suffix == ".py":
                output_file.write(f"{len(folder_list) * '\t'}{file}\n")
                folder_list.append(file)
                create_batch_file(folder_list)
                folder_list.pop()


def generate_index(filename: Path, folder_limit: int | None = None) -> None:
    print(filename)
    with open(filename, "w", encoding="utf-8") as file:
        explore_directory(file, folder_limit=folder_limit)


def main() -> None:
    generate_index(Path("hyper_index.txt"))
    generate_index(Path("index.txt"), folder_limit=1)


if __name__ == "__main__":
    main()
