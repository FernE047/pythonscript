import os
import subprocess

DIRECTORY = "C:/JavaProgs"


def contains_java_file(folder: str) -> bool:
    for filename in [f"{DIRECTORY}/{arq}" for arq in os.listdir(folder)]:
        if filename.find(".java") != -1:
            return True
    return False


def create_batch_file(filename: str) -> None:
    project_name = filename[filename.rfind("/") + 1 : filename.rfind(".")]
    batch_name = f"{DIRECTORY}/{project_name}.bat"
    print(batch_name)
    java_name = f"{filename}/{project_name}"
    with open(batch_name, "w", encoding="utf-8") as file:
        file.write(f"@echo off\njava {java_name} %*")


def create_batch_project(project_folder: str) -> None:
    project_name = project_folder[project_folder.rfind("/") + 1 :]
    batch_name = f"{DIRECTORY}/{project_name}.bat"
    print(batch_name)
    java_name = f"{project_folder}/teste.Teste"
    with open(batch_name, "w", encoding="utf-8") as file:
        file.write(f"@echo off\njava {java_name} %*")


def run_command(command: str) -> None:
    print(command)
    subprocess.Popen(command, shell=True)


def main() -> None:
    folders = os.listdir(DIRECTORY)
    folder_list = [f"{DIRECTORY}/{folder}" for folder in folders]
    for folder in folder_list:
        if contains_java_file(folder):
            run_command(f"javac {folder}/*.java")
            create_batch_file(folder)
            continue
        run_command(f"dir /s /B {folder}/*.java > {folder}/sources.txt")
        run_command(f"javac @{folder}/sources.txt")
        create_batch_project(folder)


if __name__ == "__main__":
    main()
