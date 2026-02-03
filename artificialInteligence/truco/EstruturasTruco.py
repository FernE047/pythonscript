from typing import Literal
from EstruturasBaralho import Deck
from EstruturasBaralho import Card
from random import randint

GameModeOptions = Literal["random", "highest"]


class CardsHand:
    def __init__(self) -> None:
        self.deck: list[Card] = []

    def show(self) -> None:
        for card in self.deck:
            print(str(card))

    def add(self, card: Card) -> None:
        self.deck.append(card)

    def get_card(self, index: int) -> Card:
        return self.get_cards()[index]

    def get_cards(self) -> list[Card]:
        return self.deck

    def remove_card(self, index: int) -> Card:
        return self.deck.pop(index)

    def __str__(self) -> str:
        text = ""
        for card in self.deck:
            text += str(card) + "\n"
        return text

    def __len__(self) -> int:
        return len(self.deck)


class Player:
    def __init__(self, play_order: int, is_human: bool = False) -> None:
        self.player_hand = CardsHand()
        self.is_human = is_human
        self.play_order = play_order
        shuffling_seed = "xyzSTUVWXYZ345678abcdefghijklmnopqrstuvw"
        self.unique_shuffling_seed = ""
        for _ in range(randint(10, 100)):
            self.unique_shuffling_seed += shuffling_seed[randint(0, 39)]
        self.cut_position = randint(0, 39)

    def shuffle(self, deck: Deck) -> None:
        deck.shuffle(self.unique_shuffling_seed)

    def cut(self, deck: Deck) -> None:
        deck.cut_deck(self.cut_position)

    def deal_cards(self, deck: Deck, players: list["Player"]) -> Card:
        card_turning_point = randint(1, len(players) * 3)
        card_count = 0
        leading_card = Card(0, 0)
        for _ in range(3):
            for player in players:
                player.receive_card(deck.draw_card())
                card_count += 1
                if card_count == card_turning_point:
                    leading_card = deck.draw_card()
        return leading_card

    def play_random_card(self) -> Card:
        return self.player_hand.remove_card(randint(0, len(self.player_hand) - 1))

    def play_highest_card(self, highest_rank: int) -> Card:
        highest_card_index = 0
        highest_card = self.player_hand.get_card(highest_card_index)
        for index in range(1, len(self.player_hand)):
            card = self.player_hand.get_card(index)
            if card.compare(highest_card, highest_rank) == 1:
                highest_card_index = index
                highest_card = self.player_hand.get_card(highest_card_index)
        return self.player_hand.remove_card(highest_card_index)

    def receive_card(self, card: Card) -> None:
        self.player_hand.add(card)

    def print_player(self) -> None:
        print(str(self))

    def __str__(self) -> str:
        if self.is_human:
            return f"Jogador : {self.play_order}:\n{self.player_hand}"
        return f"PC : {self.play_order}:\n{self.player_hand}"


class TrucoRound:
    def __init__(
        self, leading_card: Card, players: list[Player], initial_player_index: int
    ) -> None:
        self.players = players
        self.players_count = len(players)
        self.highest_rank = (leading_card.rank + 1) % 10
        self.round = 0
        self.leading_card = leading_card
        self.turn = initial_player_index % self.players_count
        self.round_winners = [-1, -1, -1]
        self.winners: list[int] = []
        self.rounds: list[list[Card]] = []
        self.is_draw = False

    def play_round(self, game_mode: GameModeOptions = "random") -> None:
        totalJogadores = self.players_count
        empty_card = Card(0, 0)
        current_round: list[Card] = [empty_card for _ in range(totalJogadores)]
        highest_card_index = (self.turn + 1) % totalJogadores
        is_draw = False
        print()
        for _ in range(totalJogadores):
            current_player = self.players[self.turn]
            if self.is_draw:
                current_round[self.turn] = current_player.play_highest_card(
                    self.highest_rank
                )
                self.is_draw = False
            else:
                if game_mode == "highest":
                    current_round[self.turn] = current_player.play_highest_card(
                        self.highest_rank
                    )
                else:
                    current_round[self.turn] = current_player.play_random_card()
            print(
                "Jogador "
                if current_player.is_human
                else "PC " + str(self.turn) + " : " + str(current_round[self.turn])
            )
            situation = current_round[self.turn].compare(
                current_round[highest_card_index], self.highest_rank
            )
            if situation == 1:
                highest_card_index = self.turn
                print("maior")
                is_draw = False
            elif situation == 0:
                print("empatou")
                is_draw = True
            self.turn += 1
            self.turn %= totalJogadores
        print()
        if is_draw:
            self.is_draw = True
        else:
            self.is_draw = False
            self.round_winners[self.round] = highest_card_index % totalJogadores
            self.turn = highest_card_index
        self.rounds.append(current_round)
        self.round += 1

    def is_finished(self) -> bool:
        if self.winners:
            return True
        if self.round == 0:
            return False

        def update_winners(round_index: int) -> None:
            self.winners = [
                player_index
                for player_index in range(
                    self.round_winners[round_index] % 2, self.players_count, 2
                )
            ]

        if self.round_winners[0] == -1:
            if self.round == 1:
                return False
            if self.round_winners[1] != -1:
                update_winners(1)
                return True
            if self.round == 2:
                return False
            if self.round_winners[2] == -1:
                self.winners = [
                    player_index for player_index in range(self.players_count)
                ]
                return True
            else:
                update_winners(2)
                return True
        if self.round == 1:
            return False
        if self.round_winners[1] == self.round_winners[0]:
            update_winners(0)
            return True
        if self.round_winners[1] == -1:
            update_winners(0)
            return True
        if self.round == 2:
            return False
        if self.round_winners[2] == -1:
            update_winners(0)
            return True
        update_winners(2)
        return True

    def return_cards_to_deck(self, deck: Deck) -> None:
        for game_round in self.rounds:
            for card in game_round:
                deck.add_card(card)
        for index in range(3 - self.round):
            for jogador in self.players:
                deck.add_card(jogador.player_hand.remove_card(index))
        deck.add_card(self.leading_card)

    def get_winners(self) -> list[int]:
        return self.winners

    def print_round(self) -> None:
        print(self)

    def __str__(self) -> str:
        text = ""
        for player in self.players:
            text += f"{player}\n\n"
        text += str(self.leading_card)
        return text


class Game:
    def __init__(self, num_players: Literal[4, 6]) -> None:
        self.deck = Deck()
        self.players = [Player(a) for a in range(num_players)]
        self.points = [0 for _ in range(num_players)]
        self.num_players = num_players
        self.turn = 0
        self.last_round: TrucoRound | None = None

    def jogaPartida(self, game_mode: GameModeOptions = "random") -> None:
        self.get_player(0).shuffle(self.deck)
        self.get_player(-1).cut(self.deck)
        leading_card = self.get_player(0).deal_cards(
            self.deck, [self.get_player(a) for a in range(1, self.num_players + 1)]
        )
        round = TrucoRound(leading_card, self.players, self.turn + 1)
        round.print_round()
        while not round.is_finished():
            round.play_round(game_mode=game_mode)
        winners = round.get_winners()
        print(winners)
        for winner in winners:
            self.points[winner] += 1
        round.return_cards_to_deck(self.deck)
        self.turn += 1
        self.last_round = round

    def get_player(self, indice: int) -> Player:
        return self.players[(self.turn + indice) % self.num_players]


def main() -> None:
    game = Game(6)
    game.jogaPartida()
    print(5 * "\n")
    round_counter = 1
    while 12 not in game.points:
        game.jogaPartida(game_mode="highest")
        print(5 * "\n")
        round_counter += 1
    print(game.points)
    print(round_counter)


if __name__ == "__main__":
    main()
