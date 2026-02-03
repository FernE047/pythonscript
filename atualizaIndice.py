from io import TextIOWrapper
import os
from typing import Literal

# I used to have a batch file for each python script to run it directly from terminal.


def read_python(file_name: str, imported_modules: list[str]) -> None:
    def add_imported_modules(line: str) -> None:
        if line in imported_modules:
            return
        print(file_name)
        print(line, end="")
        print()
        imported_modules.append(line)

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            line = file.readline()
            while line:
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
    except Exception as _:
        pass


def get_python_version(file_name: str) -> str | Literal[False]:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            line = file.readline()
            if line.find("#v") != -1:
                return f"C:/Users/Programador/AppData/Local/Programs/Python/Python{line[2:-1]}/python"
    except Exception as _:
        pass
    return "python"


def check_no_batch_flag(file_name: str) -> bool:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            line = file.readline()
            if line.find("#NoBatch") != -1:
                return True
    except Exception as _:
        pass
    return False


def create_batch_file(folders: list[str]) -> None:
    batch_name = f"C:/pythonscript/{folders[-1][:-3]}.bat"
    print(batch_name)
    python_file_name = "/".join(folders)
    if not check_no_batch_flag(python_file_name):
        python_exe = get_python_version(python_file_name)
        with open(batch_name, "w", encoding="utf-8") as file:
            file.write(f"@echo off\n{python_exe} {python_file_name} %*")


def filter_batch_files(file_list: list[str]) -> list[str]:
    filtered_files: list[str] = []
    for file in file_list:
        if file.lower().find(".bat") == -1:
            filtered_files.append(file)
    return filtered_files


def explore_directory(
    output_file: TextIOWrapper,
    current_folder: str | None = None,
    folder_list: list[str] | None = None,
    folder_limit: int | None = None,
) -> None:
    if current_folder is not None:
        files = os.listdir(current_folder)
    else:
        files = os.listdir("C:/pythonscript")
    if folder_list is None:
        folder_list = ["C:", "pythonscript"]
    if folder_limit is not None:
        if len(folder_list) > folder_limit:
            return None
    files = filter_batch_files(files)
    if len(files) > 100:
        return None
    for file in files:
        if file.find(".") == -1:
            output_file.write(f"{len(folder_list) * '\t'}{file}\n")
            folder_list.append(file)
            explore_directory(
                output_file,
                current_folder="/".join(folder_list),
                folder_list=folder_list,
                folder_limit=folder_limit,
            )
            folder_list.pop()
        else:
            if file.find("txt") != -1:
                output_file.write(f"{len(folder_list) * '\t'}{file}\n")
            if file[-3:] == ".py":
                output_file.write(f"{len(folder_list) * '\t'}{file}\n")
                folder_list.append(file)
                create_batch_file(folder_list)
                folder_list.pop()


def generate_index(file_name: str, folder_limit: int | None = None) -> None:
    print(file_name)
    with open(file_name, "w", encoding="utf-8") as file:
        explore_directory(file, folder_limit=folder_limit)


generate_index("hyper_index.txt")
generate_index("index.txt", folder_limit=1)
