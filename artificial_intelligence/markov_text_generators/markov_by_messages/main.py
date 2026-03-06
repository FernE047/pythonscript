from fetch_messages import extract_and_save_messages
from generate_chain import generate_markov_chain
from generate_message import generate_markov_messages

def main() -> None:
    extract_and_save_messages()
    generate_markov_chain()
    generate_markov_messages()

if __name__ == "__main__":
    main()