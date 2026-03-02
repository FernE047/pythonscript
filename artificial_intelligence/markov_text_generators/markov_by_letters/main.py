from fetch_messages import extract_and_save_messages
from generate_chain import generate_character_chain
from generate_messages import generate_messages

def main() -> None:
    extract_and_save_messages()
    generate_character_chain()
    generate_messages()

if __name__ == "__main__":
    main()