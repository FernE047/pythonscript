import subprocess


def main() -> None:
    # serve como batch pra acessar a biblioteca.py
    escolha = "s"
    while escolha == "s":
        subprocess.call("python C:\\pythonscript\\randomBranch\\randomBranchMaker.py ")
        print("você quer continuar [s|n]")
        escolha = input()


if __name__ == "__main__":
    main()