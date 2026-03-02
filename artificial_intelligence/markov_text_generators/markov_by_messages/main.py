from fetch_messages import fetch_messages
from generate_chain import generate_markov_chain
from generate_message import generate_markov_messages

def main() -> None:
    fetch_messages()
    generate_markov_chain()
    generate_markov_messages()

if __name__ == "__main__":
    main()