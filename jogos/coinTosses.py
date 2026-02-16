import random

# script done while taking a crash course in python, it is a simple coin toss game where the user has to guess the outcome of a coin toss (heads or tails) and gets two chances to guess correctly.


def main() -> None:
    guess = ""
    while guess not in ("heads", "tails"):
        print("Guess the coin toss! Enter heads or tails:")
        guess = input()
    toss = ["tails", "heads"][random.randint(0, 1)]  # 0 is tails, 1 is heads
    if toss == guess:
        print("You got it!")
        return
    print("Nope! Guess again!")
    guess = input()
    if toss == guess:
        print("You got it!")
    else:
        print("Nope. You are really bad at this game.")


if __name__ == "__main__":
    main()
