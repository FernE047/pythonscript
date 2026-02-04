import re

INPUT_FILE = "ConversaDoWhatsApp.txt"
OUTPUT_FILE = "sohMensagens.txt"
PERSON_1 = ""
DATE_PATTERN = r"([0-3][0-9][/][0-1][0-9][/]20[21][09] [0-2][0-9][:][0-5][0-9])"


def main() -> None:
    message = ""
    with (
        open(INPUT_FILE, "r", encoding="utf-8") as input_file,
        open(OUTPUT_FILE, "w", encoding="utf-8") as output_file,
    ):
        word = input_file.read(16)
        while True:
            if re.search(DATE_PATTERN, word) and len(message) > 0:
                message = message[3:-17]
                user = message[:13]
                if user == f"{PERSON_1}: ":
                    message = message[13:]
                    print(message)
                    output_file.write(message + "\n")
                message = ""
            letter = input_file.read(1)
            if not letter:
                break
            word = word[1:] + letter
            message += letter


if __name__ == "__main__":
    main()
