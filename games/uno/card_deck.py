import random
from enum import Enum

# simple script to create a deck of uno cards, it is not a complete game, it just creates the deck and shuffles it, then prints the shuffled deck.


class Color(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4


class Rank(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    SKIP = 10
    REVERSE = 11
    PLUS_TWO = 12
    WILD = 13
    WILD_PLUS_FOUR = 14


TWICE_IN_DECK = (
    Rank.ONE,
    Rank.TWO,
    Rank.THREE,
    Rank.FOUR,
    Rank.FIVE,
    Rank.SIX,
    Rank.SEVEN,
    Rank.EIGHT,
    Rank.NINE,
    Rank.SKIP,
    Rank.REVERSE,
    Rank.PLUS_TWO,
)

FOUR_IN_DECK = (Rank.WILD, Rank.WILD_PLUS_FOUR)

NORMAL_COLORS = (Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW)


class Card:
    def __init__(self, color: Color, rank: Rank) -> None:
        self.color = color
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.color.name} {self.rank.name}"


def main() -> None:
    uno: list[Card] = []
    for color in NORMAL_COLORS:
        uno.append(Card(color, Rank.ZERO))
        for rank in TWICE_IN_DECK:
            for _ in range(2):
                uno.append(Card(color, rank))
    for rank in FOUR_IN_DECK:
        for _ in range(4):
            uno.append(Card(Color.BLACK, rank))
    random.shuffle(uno)
    print(uno)


if __name__ == "__main__":
    main()
