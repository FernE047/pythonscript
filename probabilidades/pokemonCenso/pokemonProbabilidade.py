from time import time
import shelve


def main() -> None:
    with shelve.open("BDPokemonNoDetails") as dados:
        tiposCat = [
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
        ]
        soma = {}
        soma["type"] = {}
        for tipo in tiposCat:
            soma["type"][tipo] = 0
        categorias = [
            "male rate",
            "female rate",
            "height",
            "weight lbs",
            "weight kg",
            "capture rate",
            "base egg steps",
            "alola",
            "quantia tipo",
            "genderless",
            "mega",
        ]
        total = 0
        for cat in categorias:
            soma[cat] = 0
        for chaves in dados:
            total += 1
            pokemon = dados[chaves]
            # print(f"{chaves} : {pokemon}")
            tipos = pokemon["tipo"]
            for tipo in tipos:
                soma["type"][tipo] += 1
            soma["quantia tipo"] += len(tipos)
            for cat in categorias[2:-4]:
                soma[cat] += pokemon[cat]
            if pokemon["male rate"] == -1:
                soma["genderless"] += 1
            else:
                soma["male rate"] += pokemon["male rate"]
                soma["female rate"] += pokemon["female rate"]
            if pokemon["alola"]:
                soma["alola"] += 1
            if pokemon["mega"]:
                soma["mega"] += 1
        print(f"male rate : {soma['male rate'] / (total - soma['genderless'])}")
        print(
            f"female rate : {soma['female rate'] / (total - soma['genderless'])}"
        )
        for cat in categorias[2:-3]:
            print(f"{cat} : {soma[cat] / total}")
        print("")
        for tipo in tiposCat:
            porcentagem = soma["type"][tipo] * 100 / total
            print(f"{tipo} : {porcentagem}%")
        print(f"\ngenderless : {soma['genderless'] * 100 / total}%")
        print(f"\nalola : {soma['alola'] * 100 / (total - soma['alola'])}%")
        print(f"\nmega : {soma['mega'] * 100 / (total - soma['mega'])}%")
        print(f"\ntotal : {total}")


if __name__ == "__main__":
    main()
