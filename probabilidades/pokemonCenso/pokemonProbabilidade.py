from time import time
import shelve

dados = shelve.open("BDPokemonNoDetails")
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
    # print(chaves+" : "+str(pokemon))
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
print("male rate : " + str(soma["male rate"] / (total - soma["genderless"])))
print("female rate : " + str(soma["female rate"] / (total - soma["genderless"])))
for cat in categorias[2:-3]:
    print(cat + " : " + str(soma[cat] / total))
print("")
for tipo in tiposCat:
    porcentagem = soma["type"][tipo] * 100 / total
    print(tipo + " : " + str(porcentagem) + "%")
print("\ngenderless : " + str(soma["genderless"] * 100 / total) + "%")
print("\nalola : " + str(soma["alola"] * 100 / (total - soma["alola"])) + "%")
print("\nmega : " + str(soma["mega"] * 100 / (total - soma["mega"])) + "%")
print("\ntotal : " + str(total))
dados.close()
