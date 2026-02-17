from typing import Any
from PIL import Image
import pyautogui
import time
import random

# this code is too dependant on global Coordinates and Colors. I started doing it, but I give up.

# Constants

DEFAULT_WAIT = 1 / 2
STEP_WAIT_DURATION = 1 / 300
WALK_TIME_DURATION = 1 / 3
PRINT_DEBUG = True
SCREEN_START_X = 65
SCREEN_END_X = 705
SCREEN_STEP_X = 10
RED_ARROW_Y_1 = 434
RED_ARROW_Y_2 = 482
MENU_CHECK_Y_DEFAULT = 495

# Keys

KEY_UP = "i"
KEY_DOWN = "k"
KEY_LEFT = "j"
KEY_RIGHT = "l"
KEY_ENTER = "w"
KEY_A = "x"
KEY_B = "z"

CoordData = tuple[int, int]
ColorData = tuple[int, int, int]
StepData = tuple[str, int] | None
WalkData = list[StepData]

# Colors

SPEACH_BUBBLE_COLOR = (224, 8, 8)
BATTLE_RED_ARROW_COLOR = (248, 0, 0)
MENU_COLOR = (96, 96, 96)
UNKNOWN_COLOR_01 = (248, 240, 40)
ACTIVE_COLOR = (248, 208, 176)

# Coordinates

EMULATOR_POSITION = (350, 750)
RECENT_ROMS_POSITION = (81, 41)
POKEMON_ROM_POSITION = (150, 320)
CLOSE_BUTTON_POSITION = (900, 600)
UNKNOWN_COORDINATES_01 = (554, 170)
ACTIVE_COORDINATE = (367, 276)
UNKNOWN_COORDINATES_02 = (67, 104)


def print(*args: Any, **kwargs: Any) -> None:
    if PRINT_DEBUG:
        __builtins__.print(*args, **kwargs)


class AttackMove:
    # boilerplate
    def __init__(self, name: str, power: int, accuracy: int, pp: int) -> None:
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.pp = pp


class Pokemon:
    def __init__(
        self,
        name: str = "",
        gender: str = "f",
        level: int = 0,
        nature: str = "",
        pokemon_type: str = "",
        health_points: int = 0,
        special_attack: int = 0,
        special_defense: int = 0,
        attack: int = 0,
        defense: int = 9,
        speed: int = 0,
        experience_points: int = 0,
        experience_for_next_level: int = 0,
        attack_moves: list[AttackMove | None] | None = None,
    ) -> None:
        self.name = name
        self.gender = gender
        self.nature = nature
        self.level = level
        self.pokemon_type = pokemon_type
        self.health_points = health_points
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.experience_points = experience_points
        self.experience_for_next_level = experience_for_next_level
        if attack_moves is None:
            attack_moves = [None, None, None, None]
        self.attack_moves = attack_moves


class Database:
    def __init__(self) -> None:
        self.attack_moves: list[AttackMove] = []
        self.pokemons: list[Pokemon] = []
        self.player_pokemons: list[Pokemon | None] = [None] * 6
        self.jogadorItens: list[str] = []

    def clean_database(self) -> None:
        self.attack_moves = []
        self.pokemons = []
        self.player_pokemons = [None] * 6
        self.jogadorItens = []

    def colocaPokemon(self, slot: int, pokemon: Pokemon) -> None:
        self.player_pokemons[slot] = self.search_pokemon_index_by_name(pokemon.name)

    def search_pokemon_index_by_name(self, name: str) -> Pokemon | None:
        for pokemon in self.pokemons:
            if name == pokemon.name:
                return pokemon
        return None

    def delete_pokemon(self, slot: int) -> None:
        self.player_pokemons[slot] = None

    def append_pokemon(self, pokemon_to_add: Pokemon) -> None:
        self.pokemons.append(pokemon_to_add)

    def update_pokemon(
        self,
        pokemon_index: int,
        gender: str = "",
        level: int = 0,
        nature: str = "",
        pokemon_type: str = "",
        health_points: int = 0,
        special_attack: int = 0,
        special_defense: int = 0,
        attack: int = 0,
        defense: int = 9,
        speed: int = 0,
        experience_points: int = 0,
        experience_for_next_level: int = 0,
        attack_moves: list[AttackMove | None] | None = None,
    ) -> None:
        pokemon = self.pokemons[pokemon_index]
        if level != pokemon.level:
            pokemon.level = level
        if gender != pokemon.gender:
            pokemon.gender = gender
        if nature != pokemon.nature:
            pokemon.nature = nature
        if pokemon_type != pokemon.pokemon_type:
            pokemon.pokemon_type = pokemon_type
        if health_points != pokemon.health_points:
            pokemon.health_points = health_points
        if special_attack != pokemon.special_attack:
            pokemon.special_attack = special_attack
        if special_defense != pokemon.special_defense:
            pokemon.special_defense = special_defense
        if attack != pokemon.attack:
            pokemon.attack = attack
        if defense != pokemon.defense:
            pokemon.defense = defense
        if speed != pokemon.speed:
            pokemon.speed = speed
        if experience_points != pokemon.experience_points:
            pokemon.experience_points = experience_points
        if experience_for_next_level != pokemon.experience_for_next_level:
            pokemon.experience_for_next_level = experience_for_next_level
        if attack_moves is not None:
            pokemon.attack_moves = attack_moves

    def get_attack_details(self, check_attack: str) -> AttackMove:
        for attack_move in self.attack_moves:
            if attack_move.name == check_attack:
                return attack_move
        new_attack = AttackMove(name=check_attack, power=0, accuracy=0, pp=0)
        self.attack_moves.append(new_attack)
        return new_attack


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


# menus


def click(coord: tuple[int, int], wait_time: float = DEFAULT_WAIT) -> None:
    pyautogui.click(coord)
    if wait_time:
        wait(wait_time)


def launch_game() -> None:
    click(EMULATOR_POSITION)
    click(RECENT_ROMS_POSITION)
    click(POKEMON_ROM_POSITION)


def close_emulator() -> None:
    click(EMULATOR_POSITION)
    click(CLOSE_BUTTON_POSITION)


# procedimento de cutscenes


def play_intro_cutscene(database: Database) -> None:
    wait(6)
    press_key(KEY_ENTER)
    wait_color_at_position(UNKNOWN_COORDINATES_01, UNKNOWN_COLOR_01)
    wait(2)
    press_key(KEY_ENTER)
    skip_conversations(UNKNOWN_COORDINATES_02)
    skip_full_dialogue(12, (85, 195))
    skip_conversations((326, 474))
    wait_color_at_position((600, 70), (16, 112, 224))
    for _ in range(7):
        press_key(KEY_A)
    press_key(KEY_ENTER)
    skip_conversations((85, 120))
    talk_counting_red_arrows(11)
    wait_color_at_position((467, 330), (248, 248, 248))  # caminhao
    move_in_direction(KEY_RIGHT, 3)
    skip_full_dialogue(5, (289, 494))
    wait()
    skip_conversations((446, 2))
    wait()
    skip_full_dialogue(4, (401, 2))
    wait()
    move_in_direction(KEY_UP, 5)
    scene_transition()
    move_in_direction(KEY_LEFT, 2)
    move_in_direction(KEY_UP, 1)
    press_key(KEY_A)
    skip_full_dialogue(1, (464, 437))
    wait_color_at_position((100, 100), (72, 176, 184))
    press_key(KEY_A)
    press_key(KEY_UP)
    press_key(KEY_A)
    skip_full_dialogue(4, (607, 2))
    wait(2)
    move_in_direction(KEY_RIGHT, 2)
    move_in_direction(KEY_UP, 1)
    skip_conversations((359, 2))
    skip_conversations((365, 2))
    skip_conversations((650, 2))
    skip_full_dialogue(1, (175, 2))
    skip_full_dialogue(2, (540, 2))
    wait(2)
    walk_path(
        [
            (KEY_RIGHT, 4),
            (KEY_DOWN, 4),
            None,
            (KEY_RIGHT, 9),
            (KEY_UP, 1),
        ]
    )
    skip_full_dialogue(5, (570, 445))
    move_in_direction(KEY_UP, 6)
    scene_transition()
    walk_path([(KEY_DOWN, 2), (KEY_RIGHT, 3)])
    press_key(KEY_A)
    skip_full_dialogue(11, (506, 447))
    wait(2)
    walk_path(
        [
            (KEY_LEFT, 3),
            (KEY_UP, 3),
            None,
            (KEY_DOWN, 6),
            None,
            (KEY_LEFT, 3),
            (KEY_UP, 8),
        ]
    )
    skip_full_dialogue(3, (158, 2))
    move_in_direction(KEY_UP, 2)
    skip_conversations((206, 447))
    skip_full_dialogue(1, (362, 2))
    walk_path([(KEY_LEFT, 4), (KEY_UP, 1)])
    press_key(KEY_A)
    wait(1)
    inicial = random.randint(0, 2)
    print(str(inicial))
    if inicial == 1:
        press_key(KEY_RIGHT)
        starter_pokemon = Pokemon(name="mudkip", level=5)
    elif inicial == 2:
        press_key(KEY_LEFT)
        starter_pokemon = Pokemon(name="treecko", level=5)
    else:
        starter_pokemon = Pokemon(name="torchic", level=5)
    database.append_pokemon(starter_pokemon)
    wait()
    press_key(KEY_A)
    press_key(KEY_A)


# esperas


def wait(wait_time: float = DEFAULT_WAIT) -> None:
    print(f"waiting {wait_time} seconds")
    time.sleep(wait_time)


def wait_color_at_position(
    coordinates: CoordData, color: ColorData, pressed: str | None = None
) -> None:
    print(f"waiting {color} at coordinates {coordinates}")
    if pressed is not None:
        pyautogui.keyDown(pressed)
    while True:
        wait()
        screen = pyautogui.screenshot()
        if screen.getpixel(coordinates) == color:
            print("color found")
            if pressed is not None:
                pyautogui.keyUp(pressed)
            return None


def scene_transition() -> None:
    while True:
        wait()
        screen = pyautogui.screenshot()
        if screen.getpixel(ACTIVE_COORDINATE) == ACTIVE_COLOR:
            print("transition detected")
            wait(1)
            return None


# conversas


def talk_counting_red_arrows(
    arrow_count: int, target_color: ColorData = SPEACH_BUBBLE_COLOR
) -> None:
    print("talking started")
    for arrow_index in range(arrow_count):
        with pyautogui.hold(KEY_A):
            scan_for_color(target_color)
        press_key(KEY_A)
        print(f"\ttecla {KEY_A} apertada {arrow_index + 1} vezes")
    print("talking done")


def scan_for_color(target_color: ColorData) -> None:
    while True:
        tela = pyautogui.screenshot()
        for x in range(SCREEN_START_X, SCREEN_END_X, SCREEN_STEP_X):
            if tela.getpixel((x, RED_ARROW_Y_1)) == target_color:
                return None
            elif tela.getpixel((x, RED_ARROW_Y_2)) == target_color:
                return None


def skip_conversations(coord: CoordData) -> None:
    if coord[1] == 2:
        coord = (coord[0], MENU_CHECK_Y_DEFAULT)
    wait_color_at_position(coord, MENU_COLOR)
    press_key(KEY_A)


def skip_full_dialogue(dialogue_arrow_count: int, coord: CoordData) -> None:
    talk_counting_red_arrows(dialogue_arrow_count)
    skip_conversations(coord)


# andar e apertar


def press_key(key_to_press: str, hold_time: float = DEFAULT_WAIT) -> None:
    if PRINT_DEBUG:
        print(f"key {key_to_press} pressed for {hold_time} seconds'")
    with pyautogui.hold(key_to_press):
        time.sleep(hold_time)


def move_in_direction(direction: str, steps: int = 1) -> None:
    print(f"walking to {direction}")
    for step_index in range(steps):
        press_key(direction, hold_time=STEP_WAIT_DURATION)
        print(f"\t{step_index + 1} steps")
        time.sleep(WALK_TIME_DURATION)
    print("walking done")


def walk_path(path_commands: WalkData) -> None:
    for step in path_commands:
        if step is None:
            scene_transition()
            continue
        move_in_direction(step[0], step[1])


# batalhas


def decrypt_font_character(numero: int) -> str:
    valores = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789L"
    return valores[numero - 1]


class Opponent:
    def __init__(self):
        self.name = ""
        self.level = 0
        self.scanNomeInimigo()
        self.gender = self.scanGeneroInimigo()
        self.health_points = self.scanVidaInimigo()

    def scanNomeInimigo(self):
        screen = pyautogui.screenshot()
        x = 60
        opponent_name = ""
        target_color = (64, 64, 64)
        while True:
            pixel = screen.getpixel((x, 114))
            if x == 315:
                break
            elif pixel != target_color:
                x += 1
                continue
            image = Image.new("RGBA", (10, 19), (255, 255, 255, 255))
            for letter_x in range(10):
                for letter_y in range(19):
                    pixel = screen.getpixel((letter_x + x, letter_y + 114))
                    if pixel == target_color:
                        image.putpixel((letter_x, letter_y), (0, 0, 0, 255))
            is_same_letter = False
            letter_index = 0
            for current_letter_index in range(1, 38):
                try:
                    image_to_compare = open_image_as_rgba(f"./alfabeto1/{current_letter_index}.png")
                except Exception:
                    image_to_compare = False
                if image_to_compare:
                    is_same_letter = True
                    for letter_x in range(10):
                        for letter_y in range(19):
                            if image.getpixel(
                                (letter_x, letter_y)
                            ) != image_to_compare.getpixel((letter_x, letter_y)):
                                is_same_letter = False
                if is_same_letter:
                    letter_index = current_letter_index
                    break
            if not (is_same_letter):
                #saves the letter for future comparisons, asking the user to input the correct letter index
                print(opponent_name)
                print("qual o numero dessa letra?")
                letter_index = int(input())
                image.save(f"./alfabeto1/{letter_index}.png")
            opponent_name += decrypt_font_character(letter_index)
            x += 10
        for letra in range(len(opponent_name) - 1, 0, -1):
            if opponent_name[letra] == "L":
                self.name = opponent_name[:letra]
                self.level = int(opponent_name[letra + 1 :])
        return opponent_name

    def scanGeneroInimigo(self):
        tela = pyautogui.screenshot()
        for x in range(50, 320):
            pixel = tela.getpixel((x, 120))
            if pixel == (114, 203, 224):
                return "m"
            elif pixel == (0, 0, 0):
                return "f"
        return "f"

    def scanVidaInimigo(self):
        tela = pyautogui.screenshot()
        cores = [(88, 208, 128), (200, 168, 8), (168, 64, 72)]
        vida = 0
        for x in range(164, 306):
            pixel = tela.getpixel((x, 150))
            if pixel in cores:
                vida += 1
        porcentagem = int(vida * 100 / 142)
        return porcentagem

    def atualizaVida(self):
        self.health_points = self.scanVidaInimigo()


def open_image_as_rgba(image_path: str) -> Image.Image:
    with Image.open(image_path) as image:
        image_in_memory = image.copy()
        if image.mode != "RGBA":
            return image_in_memory.convert("RGBA")
        return image_in_memory


def batalha() -> None:
    talk_counting_red_arrows(1, target_color=BATTLE_RED_ARROW_COLOR)
    wait_color_at_position((400, 440), (72, 64, 80))
    opponent = Opponent()
    assert (
        opponent is not None
    )  # here just to make sure the class is being used. linter issues


def battle_update(database: Database, slot: int) -> None:
    global teclas
    press_key(KEY_DOWN)
    press_key(KEY_A)
    wait(1)
    press_key(KEY_A)
    press_key(KEY_A)
    pokemon = fetch_pokemon_data(database, slot)
    assert (
        pokemon is not None
    )  # here just to make sure the function is being used. linter issues


def fetch_pokemon_data(database: Database, slot: int) -> int:
    pokemons = database.pokemons
    indice = database.player_pokemons[slot]
    tela = pyautogui.screenshot()
    assert (
        pokemons,
        indice,
        tela,
    ) is not None  # here just to make sure the variables are being used. linter issues
    # TODO: stopped coding here
    return slot


def main() -> None:
    start_time = time.time()
    database = Database()
    database.clean_database()
    try:
        launch_game()
        play_intro_cutscene(database)
        talk_counting_red_arrows(1, target_color=BATTLE_RED_ARROW_COLOR)
        wait_color_at_position((400, 440), (72, 64, 80))
        opponent = Opponent()
        print(f"batalhando com {opponent.name}")
        print(f"level {opponent.level}")
        print(f"vida: {opponent.health_points}%")
        battle_update(database, 0)
        close_emulator()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Success\n Elapsed time:")
        print_elapsed_time(elapsed_time)
    except KeyboardInterrupt:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Interrupted. Elapsed time:")
        print_elapsed_time(elapsed_time)
        print("\nDone.")


if __name__ == "__main__":
    main()
