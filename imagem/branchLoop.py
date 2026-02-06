import subprocess


def main() -> None:
    # serve como batch pra acessar a biblioteca.py
    user_choice = "y"
    while user_choice == "y":
        subprocess.call("python C:/pythonscript/randomBranch/randomBranchMaker.py ")
        print("Are you sure you want to create another branch? (y/n)")
        user_choice = input()


if __name__ == "__main__":
    main()