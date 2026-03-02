from fetch_fanfics import fetch_and_save_fanfics
from generate_chain import generate_markov_chain
from generate_fanfic import generate_fanfiction

def main() -> None:
    fetch_and_save_fanfics()
    generate_markov_chain()
    generate_fanfiction()

if __name__ == "__main__":
    main()