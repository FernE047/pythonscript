from pathlib import Path
from typing import Literal, overload
from send2trash import send2trash
import random
import os

# TODO: add constants for file paths and other strings, there is A LOT of magic strings in this code, it is really hard to maintain, I need to change that


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


def print_module(module_path: Path) -> None:
    with (
        open(module_path / "answer.txt", "r") as answers_file,
        open(module_path / "question.txt", "r") as questions_file,
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


def edit_module(folder: Path, module: str) -> None:
    opcoes = ["Back", "New", "Edit", "Delete"]
    user_choice = choose_from_options("escolha uma opcao : ", opcoes)
    path_module = folder / module
    answer_path = path_module / "answer"
    answer_txt = answer_path.with_suffix(".txt")
    question_path = path_module / "question"
    question_txt = question_path.with_suffix(".txt")
    if user_choice in ["Edit", "Delete"]:
        print_module(path_module)
        answer_temp = answer_path.with_suffix(".txt.tmp")
        question_temp = question_path.with_suffix(".txt.tmp")
        line_count = count_lines(answer_txt)
        index_edit = int_input(
            "type the index you want to edit", minimum_value=1, maximum_value=line_count
        )
        with (
            open(answer_txt, "r") as answers_file,
            open(question_txt, "r") as questions_file,
            open(answer_temp, "w") as answers_fileTemp,
            open(question_temp, "w") as questions_fileTemp,
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
                    print(f"{index}) ")
                    print(questions_line, end="")
                    print(f"{answers_line}\n")
                answers_line = answers_file.readline()
                questions_line = questions_file.readline()
                index += 1
        send2trash(answer_txt)
        send2trash(question_txt)
        answer_temp.rename(answer_txt)
        question_temp.rename(question_txt)
    if user_choice == "New":
        print_module(path_module)
        with (
            open(answer_txt, "a") as answers_file,
            open(question_txt, "a") as questions_file,
        ):
            while True:
                question_word = input("type the question word")
                if question_word == "0":
                    return
                questions_file.write(f"{question_word}\n")
                answer_word = input("type the answer word")
                answers_file.write(f"{answer_word}\n")


def delete_module(folder: Path, module: str) -> None:
    send2trash(folder / module)
    print(f"Module Deleted {module}")


def make_question(
    questions: list[str], answers: list[str], index: int, choice: str
) -> str:
    temp_answers: list[str] | None = None
    if choice == "Respostas":
        temp_answers = answers
        answers = questions
        questions = temp_answers
        temp_answers = None
    else:
        mode = random.randint(0, 1)
        if mode:
            temp_answers = answers
            answers = questions
            questions = temp_answers
            temp_answers = None
    current_question = questions[index]
    current_answer = answers[index]
    answer = input(current_question[:-1])
    if answer == "0":
        return answer
    if answer == current_answer[:-1]:
        print("\tCongratulations!!!\n")
    else:
        print("\tWrong\n")
    return answer


def count_lines(fileName: Path) -> int:
    with open(fileName, "r") as file:
        lines = file.read().splitlines()
    return len(lines)


def study_module(folder: Path, module: str) -> None:
    module_path = folder / module
    answer_txt = module_path / "answer.txt"
    quantity = count_lines(answer_txt)
    options = ["Back", "Questions", "Answers", "Questions & Answers"]
    user_choice = choose_from_options("choose a mode : ", options)
    print("type 0 anywhere to exit")
    question_txt = module_path / "question.txt"
    with (
        open(answer_txt, "r") as answers_file,
        open(question_txt, "r") as questions_file,
    ):
        answers = answers_file.read().splitlines()
        questions = questions_file.read().splitlines()
    while True:
        index = random.randint(0, quantity - 1)
        answer = make_question(questions, answers, index, user_choice)
        if answer == "0":
            return


def new_module(folder: Path, evaluation_folder: Path, module: str) -> None:
    path_module = folder / module
    print(path_module)
    if path_module.exists():
        print("já existe")
        return
    path_module.mkdir()
    evaluation_module = evaluation_folder / module
    evaluation_module.mkdir(exist_ok=True)
    answer_txt = path_module / "answer.txt"
    question_txt = path_module / "question.txt"
    with (
        open(answer_txt, "w") as answers_file,
        open(question_txt, "w") as questions_file,
    ):
        print("type 0 to stop")
        while True:
            word = input("type the question word: ")
            if word == "0":
                return
            questions_file.write(f"{word}\n")
            word = input("type the answer word: ")
            answers_file.write(f"{word}\n")


def random_study(
    folder: Path, mode: str
) -> None:  # TODO implement partial modular mode
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
                count_lines(folder / module / "answer.txt") for module in modules
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
        module_path = folder / module
        answer_txt = module_path / "answer.txt"
        question_txt = module_path / "question.txt"
        index = random.randint(0, count_lines(answer_txt) - 1)
        with (
            open(answer_txt, "r") as answers_file,
            open(question_txt, "r") as questions_file,
        ):
            answers = answers_file.read().splitlines()
            questions = questions_file.read().splitlines()
        answer = make_question(questions, answers, index, choice)
        if answer == "0":
            return


def main() -> None:
    categories_folder = Path("./categories")
    categories_folder.mkdir(exist_ok=True)
    evaluations_folder = Path("./evaluations")
    evaluations_folder.mkdir(exist_ok=True)
    while True:
        user_choice = choose_from_options(
            "choose a category : ",
            ["Exit", "Create New"] + os.listdir(categories_folder),
        )
        if user_choice == "Exit":
            return
        if user_choice == "Create New":
            new_category_name = input("type the new category name : ")
            folder = categories_folder / new_category_name.title()
            evaluation_folder = evaluations_folder / new_category_name.title()
            print(folder)
            if not folder.exists():
                folder.mkdir()
                evaluation_folder.mkdir()
            else:
                print("already exists")
            continue
        folder = categories_folder / user_choice
        evaluation_folder = evaluations_folder / user_choice
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
                        print_module(folder / module)
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
