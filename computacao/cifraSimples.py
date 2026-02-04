from string import ascii_uppercase
from string import ascii_lowercase

MAX_LETTERS = len(ascii_lowercase)


def shift_letter(letter: str, shift_amount: int) -> str:
    shift_amount %= MAX_LETTERS
    if letter in ascii_lowercase:
        lowercase_letters = list(ascii_lowercase)
        index = (shift_amount + lowercase_letters.index(letter)) % MAX_LETTERS
        return lowercase_letters[index]
    if letter not in ascii_uppercase:
        return letter
    uppercase_letters = list(ascii_uppercase)
    index = (shift_amount + uppercase_letters.index(letter)) % MAX_LETTERS
    return uppercase_letters[index]


def cipher_text(input_text: str, shift_amount: int) -> str:
    encrypted_text = ""
    for char in list(input_text):
        encrypted_text += shift_letter(char, shift_amount)
    return encrypted_text


def print_all_ciphers(input_text: str) -> None:
    print(f"{input_text}\n")
    for shift_amount in range(1, MAX_LETTERS):
        print(f"{shift_amount:02d}:")
        encrypted_text = cipher_text(input_text, shift_amount)
        print(f"{encrypted_text}\n")


def main() -> None:
    text = input("type something and we will cypher!!!: \n")
    print_all_ciphers(text)


if __name__ == "__main__":
    main()
