from random import randint
from typing import Any, Literal, cast

SuitOptions = Literal[0, 1, 2, 3]
RankOptions = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class Card:
    def __init__(self, suit: SuitOptions, rank: RankOptions) -> None:
        self.suit = suit
        self.rank = rank

    def compare(self, obj: Any, leading_card: "Card") -> Literal[-1, 0, 1]:
        if not isinstance(obj, Card):
            return 1
        if self.rank == leading_card.rank:
            if obj.rank != leading_card.rank:
                return 1
            if self.suit > obj.suit:
                return 1
            else:
                return -1
        if obj.rank == leading_card.rank:
            return -1
        if self.rank > obj.rank:
            return 1
        if obj.rank == self.rank:
            return 0
        return -1

    def show(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        text = ""
        ranks = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        suits = ["Ouro", "Espadilha", "Copas", "Paus"]
        text += ranks[self.rank]
        text += " "
        text += suits[self.suit]
        return text

    def __eq__(self, other_card: Any) -> bool:
        if not isinstance(other_card, Card):
            return False
        if self.suit != other_card.suit:
            return False
        if self.rank != other_card.rank:
            return False
        return True


class Deck:
    def __init__(self) -> None:
        self.deck: list[Card] = []
        for rank in range(10):
            for suit in range(4):
                suit_ = cast(SuitOptions, suit)
                rank_ = cast(RankOptions, rank)
                carta = Card(suit_, rank_)
                self.deck.append(carta)

    def shuffle(self, seed: str) -> None:
        for char in list(seed):
            card = self.deck.pop(ord(char) % 40)
            self.deck = [card] + self.deck

    def cut_deck(self, cut_position: int = -1) -> None:
        if cut_position < 0:
            cut_total = randint(0, len(self) - 1)
        else:
            cut_total = cut_position
        for _ in range(cut_total):
            self.add_card(self.draw_card())

    def show(self) -> None:
        print(str(self))

    def draw_card(self, from_top: bool = True) -> Card:
        if from_top:
            return self.deck.pop(0)
        else:
            return self.deck.pop(-1)

    def add_card(self, card: Card, bottom: bool = True) -> None:
        if bottom:
            self.deck = self.deck + [card]
        else:
            self.deck = [card] + self.deck

    def __len__(self):
        return len(self.deck)

    def __str__(self) -> str:
        texto = ""
        for index, card in enumerate(self.deck):
            texto += ("0" + str(index) if index < 10 else str(index)) + " : " + str(card) + "\n"
        return texto

    def __eq__(self, other_deck: Any) -> bool:
        if isinstance(other_deck, Deck) is False:
            return False
        for index, card in enumerate(self.deck):
            if card != other_deck.deck[index]:
                return False
        return True
