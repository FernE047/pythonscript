from time import time
import shelve
from typing import Any, TypedDict, cast
import requests
import bs4

SEREBII_URL = "https://www.serebii.net/pokedex-sm/{0:03d}.shtml"
TOTAL = 809
PRIMAL_CASES = (383,)
ULTRA_CASES = (800,)


class PokemonData(TypedDict):
    type: list[str]
    name: str
    male_rate: float
    female_rate: float
    height: float
    weight_lbs: float
    weight_kg: float
    capture_rate: int
    base_egg_steps: int
    is_alolan: bool
    is_mega: bool


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


def get_pokemon_type(
    data: bs4.Tag, is_alolan_form: bool, is_mega_evolution: bool = False
) -> list[str]:
    def get_types(data: bs4.Tag) -> list[str]:
        pokemon_types: list[str] = []
        image_tags = data.select("img")
        for info in image_tags:
            tipo = info.get("alt")
            if tipo is None:
                continue
            tipo = cast(str, tipo)
            pokemon_types.append(tipo[:-5])
        return pokemon_types

    if not is_mega_evolution:
        tr_tag = data.select("tr")
        if tr_tag:
            if is_alolan_form:
                data = tr_tag[1]
            else:
                data = tr_tag[0]
    return get_types(data)


def remove_whitespace(text: str) -> str:
    for space_character in [" ", "\n", "\t"]:
        if space_character in text:
            text = text.replace(space_character, "")
    return text


def sanitize_information(pokemon_data: list[bs4.Tag]) -> dict[int, str]:
    pokemon_data.pop(1)
    pokemon_data.pop(1)
    pokemon_data.pop(2)
    clean_data: dict[int, str] = {}
    for index in range(6):
        clean_data[index] = remove_whitespace(pokemon_data[index].getText())
    return clean_data


def search_mega_indexes(
    tags: list[bs4.Tag], nome: str, pokemon_index: int
) -> list[int]:
    indexes: list[int] = []
    for index, tag in enumerate(tags):
        if tag.getText().find(nome) != -1:
            indexes.append(index)
    if len(indexes) % 2 == 1:
        # special case for mega rayquaza, which has only one mega evolution but two entries in the information table
        if len(indexes) > 1:
            return indexes[1:]
        return indexes
    if pokemon_index > 300:
        # special case for mega charizard, which has two mega evolutions but three entries in the information table
        return indexes[1:]
    return indexes


def capture_data(info: dict[int, str], is_alolan_form: bool = False) -> PokemonData:
    pokemon_data: PokemonData = {
        "type": [],
        "name": info[0],
        "male_rate": 0.0,
        "female_rate": 0.0,
        "height": 0.0,
        "weight_lbs": 0.0,
        "weight_kg": 0.0,
        "capture_rate": 0,
        "base_egg_steps": 0,
        "is_alolan": False,
        "is_mega": False,
    }
    if info[1].find("Genderless") != -1:
        pokemon_data["male_rate"] = -1
        pokemon_data["female_rate"] = -1
    else:
        rate = info[1].split()
        porcento = rate[1].index("%")
        pokemon_data["male_rate"] = float(rate[1][2:porcento])
        porcento = rate[2].index("%")
        pokemon_data["female_rate"] = float(rate[2][2:porcento])
    height = info[2].split()
    if is_alolan_form:
        pokemon_data["height"] = float(height[-1][:-1])
    elif info[2].find("/") == -1:
        pokemon_data["height"] = float(height[1][:-1])
    else:
        pokemon_data["height"] = float(height[-3][:-1])
    weight = info[3].split()
    if is_alolan_form:
        pokemon_data["weight_lbs"] = float(weight[2][:-3])
        pokemon_data["weight_kg"] = float(weight[-1][:-2])
    else:
        pokemon_data["weight_lbs"] = float(weight[0][:-3])
        if info[2].find("/") == -1:
            pokemon_data["weight_kg"] = float(weight[1][:-2])
        else:
            pokemon_data["weight_kg"] = float(weight[-3][:-2])
    try:
        pokemon_data["capture_rate"] = int(info[4])
    except ValueError:
        pokemon_data["capture_rate"] = int(info[4].split()[0])
    egg = list(info[5])
    while "," in egg:
        egg.pop(egg.index(","))
    pokemon_data["base_egg_steps"] = int("".join(egg))
    pokemon_data["is_alolan"] = False
    pokemon_data["is_mega"] = False
    return pokemon_data


def log_pokemon_data(pokemon_data: PokemonData, pokemon_index: int) -> None:
    print(f"pokemon : {pokemon_index:03d}")
    for key, value in pokemon_data.items():
        print(f"{key} : {value}")
    print("")


def process_pokemon_record(database: shelve.Shelf[Any], pokemon_index: int) -> None:
    serebii_url = SEREBII_URL.format(pokemon_index)
    response = requests.get(serebii_url)
    while response.status_code != requests.codes.ok:
        response = requests.get(serebii_url)
    parsed_html = bs4.BeautifulSoup(response.text, features="html.parser")
    del response
    raw_information = parsed_html.select(".fooinfo")
    pokemon_type_data_raw = parsed_html.select(".cen")
    pokemon_type_data = [pokemon_type_data_raw[a] for a in [0, -2, -1]]
    mega_evolution_images = [
        pokemon_type_data[-1].select("img"),
        pokemon_type_data[-2].select("img"),
    ]
    pokemon_type = get_pokemon_type(pokemon_type_data[0], False)
    extracted_data = sanitize_information(raw_information[1:10])
    pokemon_data = capture_data(extracted_data)
    pokemon_data["type"] = pokemon_type
    if pokemon_index < 150:
        is_alolan_form = extracted_data[2].find("/") != -1
    else:
        is_alolan_form = False
    database[f"{pokemon_index:03d}"] = pokemon_data
    log_pokemon_data(pokemon_data, pokemon_index)
    if is_alolan_form:
        pokemon_data = capture_data(extracted_data, is_alolan_form=is_alolan_form)
        pokemon_type_data = parsed_html.select(".cen")
        pokemon_type = get_pokemon_type(pokemon_type_data[0], True)
        pokemon_data["name"] = f"Alolan {pokemon_data['name']}"
        pokemon_data["type"] = pokemon_type
        pokemon_data["is_alolan"] = is_alolan_form
        database[f"{pokemon_index:03d}Alolan"] = pokemon_data
        log_pokemon_data(pokemon_data, pokemon_index)
        return
    is_mega = mega_evolution_images[0] or mega_evolution_images[1]
    if not is_mega:
        return
    suffix = "Mega"
    if pokemon_index in ULTRA_CASES:
        suffix = "Ultra"
        mega_evolution_images.pop(1)
    elif pokemon_index in PRIMAL_CASES:
        suffix = "Primal"
    mega_evolution_name = f"{suffix} {pokemon_data['name']}"
    mega_index_list = search_mega_indexes(
        raw_information, mega_evolution_name, pokemon_index
    )
    for index, img_tag in enumerate(mega_evolution_images):
        if not img_tag:
            continue
        current_index = mega_index_list[index]
        extracted_data = sanitize_information(
            raw_information[current_index : current_index + 9]
        )
        pokemon_data = capture_data(extracted_data)
        pokemon_type = get_pokemon_type(img_tag[0], False, is_mega_evolution=True)
        pokemon_data["type"] = pokemon_type
        pokemon_data["is_mega"] = True
        database[f"{pokemon_index:03d}{suffix}"] = pokemon_data
        log_pokemon_data(pokemon_data, pokemon_index)


def main() -> None:
    with shelve.open("BDPokemonNoDetails") as database:
        try:
            for pokemon_index in range(TOTAL + 1):
                start_time = time()
                process_pokemon_record(database, pokemon_index)
                duracao = time() - start_time
                print_elapsed_time(duracao)
                print("falta = ")
                print_elapsed_time(duracao * (TOTAL - pokemon_index))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
