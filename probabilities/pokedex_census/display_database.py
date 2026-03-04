import shelve
from typing import cast
from main import PokemonData

ALL_TYPES = (
    "Normal",
    "Fire",
    "Water",
    "Grass",
    "Ice",
    "Dark",
    "Steel",
    "Electric",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Fairy",
)
COLLECTED_CATEGORIES = (
    "male_rate",
    "female_rate",
    "height",
    "weight_lbs",
    "weight_kg",
    "capture_rate",
    "base_egg_steps",
    "is_alolan",
    "quantia_tipo",
    "genderless",
    "is_mega",
)


def main() -> None:
    with shelve.open("BDPokemonNoDetails") as database:
        counters: dict[str, float] = {}
        type_counters: dict[str, int] = {}
        for pkm_type in ALL_TYPES:
            type_counters[pkm_type] = 0
        total = 0
        for category in COLLECTED_CATEGORIES:
            counters[category] = 0.0
        for chaves in database:
            total += 1
            pokemon = cast(PokemonData, database[chaves])
            types = pokemon["type"]
            for pkm_type in types:
                type_counters[pkm_type] += 1
            counters["quantia_tipo"] += len(types)
            for category in COLLECTED_CATEGORIES[2:-4]:
                counters[category] += pokemon[category]  # type: ignore
            if pokemon["male_rate"] == -1:
                counters["genderless"] += 1
            else:
                counters["male_rate"] += pokemon["male_rate"]
                counters["female_rate"] += pokemon["female_rate"]
            if pokemon["is_alolan"]:
                counters["is_alolan"] += 1
            if pokemon["is_mega"]:
                counters["is_mega"] += 1
        print(f"male_rate : {counters['male_rate'] / (total - counters['genderless'])}")
        print(
            f"female_rate : {counters['female_rate'] / (total - counters['genderless'])}"
        )
        for category in COLLECTED_CATEGORIES[2:-3]:
            print(f"{category} : {counters[category] / total}")
        print("")
        for pkm_type in ALL_TYPES:
            porcentagem = type_counters[pkm_type] * 100 / total
            print(f"{pkm_type} : {porcentagem}%")
        print(f"\ngenderless : {counters['genderless'] * 100 / total}%")
        print(
            f"\nis_alolan : {counters['is_alolan'] * 100 / (total - counters['is_alolan'])}%"
        )
        print(
            f"\nis_mega : {counters['is_mega'] * 100 / (total - counters['is_mega'])}%"
        )
        print(f"\ntotal : {total}")


if __name__ == "__main__":
    main()
