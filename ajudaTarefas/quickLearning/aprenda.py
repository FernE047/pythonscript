from io import TextIOWrapper
from typing import Literal, overload
from send2trash import send2trash
import random
import os


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text"]
) -> str: ...


@overload
def choose_from_options(
    prompt: str, options: list[str], mode: Literal["number"]
) -> int: ...


@overload
def choose_from_options(prompt: str, options: list[str]) -> str: ...


def choose_from_options(
    prompt: str, options: list[str], mode: Literal["text", "number"] = "text"
) -> str | int:
    while True:
        for i, option in enumerate(options):
            print(f"{i} - {option}")
        user_choice = input(prompt)
        try:
            if mode == "number":
                return int(user_choice)
            else:
                return options[int(user_choice)]
        except (ValueError, IndexError):
            user_choice = input("not valid, try again: ")


def int_input(
    prompt_message: str,
    minimum_value: int | None = None,
    maximum_value: int | None = None,
) -> int:
    while True:
        entry = input(f"{prompt_message} : ")
        try:
            value = int(entry)
            if (minimum_value is not None) and (value < minimum_value):
                print(f"value must be greater than or equal to {minimum_value}")
                continue
            if (maximum_value is not None) and (value > maximum_value):
                print(f"value must be less than or equal to {maximum_value}")
                continue
            return value
        except Exception as _:
            print("invalid value, please try again")


# simple system to register answers and questions
# the user can create categories and modules
# each module has a question and answer file
# the user can study the modules in random order


def print_module(module_path: str) -> None:
    with (
        open(f"{module_path}/answer.txt", "r") as answers_file,
        open(f"{module_path}/question.txt", "r") as questions_file,
    ):
        answers_line = answers_file.readline()
        questions_line = questions_file.readline()
        index = 1
        while answers_line:
            print(f"{index}) ")
            print(questions_line, end="")
            print(f"{answers_line}\n")
            answers_line = answers_file.readline()
            questions_line = questions_file.readline()
            index += 1


def edit_module(folder: str, module: str) -> None:
    opcoes = ["Back", "New", "Edit", "Delete"]
    user_choice = choose_from_options("escolha uma opcao : ", opcoes)
    path_module = f"{folder}/{module}"
    if user_choice in ["Edit", "Delete"]:
        print_module(path_module)
        line_count = count_lines(f"{path_module}/answer.txt")
        index_edit = int_input(
            "type the index you want to edit", minimum_value=1, maximum_value=line_count
        )
        with (
            open(f"{path_module}/answer.txt", "r") as answers_file,
            open(f"{path_module}/question.txt", "r") as questions_file,
            open(f"{path_module}/answer.txt.tmp", "w") as answers_fileTemp,
            open(f"{path_module}/question.txt.tmp", "w") as questions_fileTemp,
        ):
            answers_line = answers_file.readline()
            questions_line = questions_file.readline()
            index = 1
            while answers_line:
                if index == index_edit:
                    if user_choice == "Edit":
                        question_word = input("type the question word")
                        questions_fileTemp.write(f"{question_word}\n")
                        answer_word = input("type the answer word")
                        answers_fileTemp.write(f"{answer_word}\n")
                else:
                    answers_fileTemp.write(answers_line)
                    questions_fileTemp.write(questions_line)
                    print(index, end=") \n")
                    print(questions_line, end="")
                    print(answers_line + "\n")
                answers_line = answers_file.readline()
                questions_line = questions_file.readline()
                index += 1
        send2trash(f"{path_module}/answer.txt")
        send2trash(f"{path_module}/question.txt")
        os.rename(
            f"{path_module}/answer.txt.tmp",
            f"{path_module}/answer.txt",
        )
        os.rename(
            f"{path_module}/question.txt.tmp",
            f"{path_module}/question.txt",
        )
    if user_choice == "New":
        print_module(path_module)
        with (
            open(f"{path_module}/answer.txt", "a") as answers_file,
            open(f"{path_module}/question.txt", "a") as questions_file,
        ):
            while True:
                question_word = input("type the question word")
                if question_word == "0":
                    return
                questions_file.write(f"{question_word}\n")
                answer_word = input("type the answer word")
                answers_file.write(f"{answer_word}\n")


def delete_module(folder: str, module: str) -> None:
    send2trash(f"{folder}/{module}")
    print(f"Module Deleted {module}")


def make_question(
    file_a: TextIOWrapper, file_b: TextIOWrapper, index: int, choice: str
) -> str:
    file_c: TextIOWrapper | None = None
    if choice == "Respostas":
        file_c = file_b
        file_b = file_a
        file_a = file_c
        file_c = None
    else:
        mode = random.randint(0, 1)
        if mode:
            file_c = file_b
            file_b = file_a
            file_a = file_c
            file_c = None
    line_a = file_a.readline()
    line_b = file_b.readline()
    current_index = 0
    while line_a:
        if index == current_index:
            answer = input(line_a[:-1])
            if answer == "0":
                return answer
            if answer == line_b[:-1]:
                print("\tCongratulations!!!\n")
            else:
                print("\tWrong\n")
            return answer
        line_a = file_a.readline()
        line_b = file_b.readline()
        current_index += 1
    return ""


def count_lines(fileName: str) -> int:
    with open(fileName, "r") as file:
        line = file.readline()
        line_count = 0
        while line:
            line_count += 1
            line = file.readline()
    return line_count


def study_module(folder: str, module: str) -> None:
    module_path = f"{folder}/{module}"
    quantity = count_lines(f"{module_path}/answer.txt")
    options = ["Back", "Questions", "Answers", "Questions & Answers"]
    user_choice = choose_from_options("choose a mode : ", options)
    print("type 0 anywhere to exit")
    while True:
        with (
            open(f"{module_path}/answer.txt", "r") as answers_file,
            open(f"{module_path}/question.txt", "r") as questions_file,
        ):
            index = random.randint(0, quantity)
            answer = make_question(questions_file, answers_file, index, user_choice)
        if answer == "0":
            return


def new_module(folder: str, evaluation_folder: str, module: str) -> None:
    path_module = f"{folder}/{module}"
    print(path_module)
    if os.path.exists(path_module):
        print("já existe")
        return
    os.makedirs(path_module)
    os.makedirs(f"{evaluation_folder}/{module}")
    with (
        open(f"{path_module}/answer.txt", "w") as answers_file,
        open(f"{path_module}/question.txt", "w") as questions_file,
    ):
        print("type 0 to stop")
        while True:
            word = input("type the question word: ")
            if word == "0":
                return
            questions_file.write(word + "\n")
            word = input("type the answer word: ")
            answers_file.write(word + "\n")


def random_study(folder: str, mode: str) -> None:  # TODO implement partial modular mode
    modules = os.listdir(folder)
    options = ["Back", "Questions", "Answers", "Questions & Answers"]
    choice = choose_from_options("choose a mode : ", options)
    print("type 0 anywhere to exit")
    isPartial = mode.find("Partial") != -1
    if isPartial:
        mode = mode[8:]
        while True:
            options = ["Conclude Selection"]
            index = choose_from_options(
                "choose which modules to remove : ", options + modules, mode="number"
            )
            if index == 0:
                break
            if len(modules) == 1:
                print("it is not possible to remove the last module")
                break
            modules.pop(index - 1)
    while True:
        if mode == "Total":
            quantities: list[int] = [
                count_lines(f"{folder}/{a}/answer.txt") for a in modules
            ]
            sum_ = 0
            index = -1
            required_line = random.randint(1, sum(quantities))
            while sum_ < required_line:
                index += 1
                sum_ += quantities[index]
            module = modules[index]
        else:
            module = modules[random.randint(0, len(modules) - 1)]
        module_path = f"{folder}/{module}"
        index = random.randint(0, count_lines(f"{module_path}/answer.txt"))
        with (
            open(f"{module_path}/answer.txt", "r") as answers_file,
            open(f"{module_path}/question.txt", "r") as questions_file,
        ):
            answer = make_question(questions_file, answers_file, index, choice)
        if answer == "0":
            return


def main() -> None:
    while True:
        user_choice = choose_from_options(
            "choose a category : ", ["Exit", "Create New"] + os.listdir("./categories")
        )
        if user_choice == "Exit":
            return
        if user_choice == "Create New":
            new_category_name = input("type the new category name : ")
            folder = f"./categories/{new_category_name.title()}"
            evaluation_folder = f"./evaluations/{new_category_name.title()}"
            print(folder)
            if not os.path.exists(folder):
                os.makedirs(folder)
                os.makedirs(evaluation_folder)
            else:
                print("already exists")
            continue
        folder = "./categories/" + user_choice
        evaluation_folder = "./evaluations/" + user_choice
        while True:
            options = ["Back"]
            options += ["Modules"]
            if len(os.listdir(folder)) != 0:
                options += ["Random"]
            user_choice = choose_from_options("choose an option : ", options)
            if user_choice == "Back":
                break
            if user_choice == "Modules":
                while True:
                    options = ["Back"]
                    options += ["New"]
                    categories = os.listdir(folder)
                    user_choice = choose_from_options(
                        "choose an option : ", options + categories
                    )
                    if user_choice == "Back":
                        break
                    if user_choice == "New":
                        module = input("type the new module name : ")
                        new_module(folder, evaluation_folder, module.title())
                        continue
                    module = user_choice
                    options = ["Back"]
                    options += ["View"]
                    options += ["Study"]
                    options += ["Edit"]
                    options += ["Delete"]
                    user_choice = choose_from_options("choose an option : ", options)
                    if user_choice == "View":
                        print_module(f"{folder}/{module}")
                    if user_choice == "Edit":
                        edit_module(folder, module)
                    if user_choice == "Delete":
                        delete_module(folder, module)
                    if user_choice == "Study":
                        study_module(folder, module)
            if user_choice == "Random":
                modules = os.listdir(folder)
                options = ["Back", "Total"]
                if len(modules) > 1:
                    options.extend(["Simple", "Partial Total", "Partial Simple"])
                while True:
                    user_choice = choose_from_options("choose an option : ", options)
                    if user_choice == "Back":
                        break
                    random_study(folder, user_choice)


if __name__ == "__main__":
    main()
