import random
import time

# simple twenty one game

TARGET_VALUE = 21
NUMERIC_CARDS = 10
SPECIAL_CARDS = ["Q", "J", "K"]
SPECIAL_CARDS_SCORE = 10
CARDS_REPEATED = 4
PLAYER_INDEX = 0
DEALER_INDEX = 1
TIME_INTERVAL = 1.0
SPECIAL_NEW_LINES = 3
LINESPACING = SPECIAL_NEW_LINES * "\n"
INITIAL_SCORES = [0, 0]

DeckData = list[str | int]
HandData = DeckData
HandsData = list[HandData]


def display_player_hands(player_hands: HandsData, player: int) -> int:
    hand_score = 0
    hand_representation = ""
    for current_card in player_hands[player]:
        hand_representation += f"{current_card},"
        if current_card in SPECIAL_CARDS:
            hand_score += SPECIAL_CARDS_SCORE
            continue
        hand_score += int(current_card)
    hand_representation += f"\b {LINESPACING}Score : {hand_score}"
    print(hand_representation)
    return hand_score


def initialize_deck() -> DeckData:
    card_deck: DeckData = []
    for card_index in range(1, NUMERIC_CARDS + 1):
        card_deck += [card_index]
    card_deck += SPECIAL_CARDS
    card_deck *= CARDS_REPEATED
    random.shuffle(card_deck)
    return card_deck


def play_player_turn(
    card_deck: DeckData,
    player_scores: list[int],
    player_hands: HandsData,
) -> None:
    while True:
        print("your hand :")
        player_scores[PLAYER_INDEX] = display_player_hands(player_hands, PLAYER_INDEX)
        if player_scores[PLAYER_INDEX] > TARGET_VALUE:
            print(f"\nEXPLODED{LINESPACING}")
            return
        if player_scores[PLAYER_INDEX] == TARGET_VALUE:
            print(f"\nYOU WIN{LINESPACING}")
            return
        print("would you like to draw another card? [y/n]")
        user_input = input().lower()
        if user_input != "y":
            return
        player_hands[PLAYER_INDEX].append(card_deck.pop())


def is_end_game(player_scores: list[int]) -> bool:
    if player_scores[DEALER_INDEX] > TARGET_VALUE:
        print(f"\nDEALER EXPLODED{LINESPACING}", end="")
        if player_scores[PLAYER_INDEX] < TARGET_VALUE:
            print(f"{LINESPACING}YOU WIN\n")
            return True
        if player_scores[PLAYER_INDEX] >= player_scores[DEALER_INDEX]:
            print(f"{LINESPACING}YOU LOSE\n")
            return True
        print(f"{LINESPACING}YOU WIN\n")
        return True
    if player_scores[DEALER_INDEX] == TARGET_VALUE:
        print(f"\nDEALER WINS{LINESPACING}YOU LOSE\n")
        return True
    return False


def play_dealer_turn(
    card_deck: DeckData, player_scores: list[int], player_hands: HandsData
) -> None:
    if player_scores[PLAYER_INDEX] == TARGET_VALUE:
        print(f"{LINESPACING}YOU WIN\n")
        return
    while True:
        player_hands[DEALER_INDEX].append(card_deck.pop())
        print("dealer hand:")
        player_scores[DEALER_INDEX] = display_player_hands(player_hands, DEALER_INDEX)
        time.sleep(TIME_INTERVAL)
        if is_end_game(player_scores):
            return


def play_game() -> None:
    card_deck = initialize_deck()
    player_scores = INITIAL_SCORES.copy()
    player_hands: HandsData = [[card_deck.pop()], []]
    play_player_turn(card_deck, player_scores, player_hands)
    play_dealer_turn(card_deck, player_scores, player_hands)


def main() -> None:
    while True:
        play_game()
        print("play again? [y/n]")
        user_input = input().lower()
        if user_input != "y":
            break


if __name__ == "__main__":
    main()
