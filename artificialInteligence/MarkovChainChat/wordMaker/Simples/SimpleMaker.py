#type: ignore

"""
this code is beyond broken. this is her grave. let it rest in peace...
"""

from numpy.random import choice


def randomMidVowels():
    global letras
    global vowel_frequencies
    letrasPossiveis = letras[0:5]
    return choice(letrasPossiveis, 1, p=vowel_frequencies)[0]


def randomMidCons():
    global letras
    global consonant_frequencies
    letrasPossiveis = letras[5:]
    return choice(letrasPossiveis, 1, p=consonant_frequencies)[0]


def firstLetter():
    global letras
    global initial_letter_occurrences
    letraAdicional = ""
    letra = choice(letras, 1, p=initial_letter_occurrences)[0]
    if letra == "q":
        letraAdicional = "u"
    if letra in ["b", "c", "d", "f", "g", "k", "p", "t", "v"]:
        chanceAdicional = choice([0, 1], 1, p=[0.95, 0.05])
        if chanceAdicional:
            letraAdicional = randomMidCons()
            while letraAdicional not in ["l", "r", "h"]:
                letraAdicional = randomMidCons()
    return letra + letraAdicional


def randomEnd(quant, isFirstVowel=True):
    mid = ""
    consoanteAdicional = 0
    for a in range(quant):
        if (bool(a % 2)) == isFirstVowel:
            mid += randomMidVowels()
            consoanteAdicional = 0
        else:
            letra = randomMidCons()
            if letra == "q":
                mid += "qu"
            elif letra in ["l", "s", "r", "y", "w", "z", "x", "n", "m"]:
                if not (consoanteAdicional):
                    consoanteAdicional = choice([0, 1], 1, p=[0.75, 0.25])[0]
                    if consoanteAdicional:
                        isFirstVowel = not (isFirstVowel)
                mid += letra
            else:
                mid += letra
                if letra not in ["h", "j"]:
                    consoanteAdicional = choice([0, 1], 1, p=[0.95, 0.05])
                    if consoanteAdicional:
                        letra = randomMidCons()
                        while letra not in ["l", "r", "h"]:
                            letra = randomMidCons()
                        mid += letra
    return mid


def makeSubWord(tamanhos, tamanhoStats):
    lenght = choice(tamanhos, 1, p=tamanhoStats)[0]
    begin = firstLetter()
    end = randomEnd(lenght - 1, isFirstVowel=(begin in ["a", "e", "i", "o", "u"]))
    return begin + end


def generate_word() -> str:
    global word_counts
    global word_stats
    global word_length_frequencies
    global word_lengths
    words_quantity = choice(word_counts, 1, p=word_stats)[0]
    words: list[str] = []
    for word_index in range(words_quantity):
        index = word_counts.index(word_index + 1)
        usedWordSizes = word_lengths[index]
        usedWordSizeStats = word_length_frequencies[index]
        words.append(makeSubWord(usedWordSizes, usedWordSizeStats))
    return " ".join(words)


def normalize_statistics(frequency_map: list[int]) -> list[float]:
    total_frequency = sum(frequency_map)
    frequency_normalized = [frequency / total_frequency for frequency in frequency_map]
    while sum(frequency_normalized) != 1:
        if sum(frequency_normalized) > 1:
            add = sum(frequency_normalized) - 1
            frequency_normalized[
                frequency_normalized.index(max(frequency_normalized))
            ] -= add
        elif sum(frequency_normalized) < 1:
            add = 1 - sum(frequency_normalized)
            frequency_normalized[
                frequency_normalized.index(min(frequency_normalized))
            ] += add
    return frequency_normalized


def get_file_name() -> str:
    is_file_name_valid = True
    file_name = "default"
    while is_file_name_valid:
        print("type the file name (without .txt): ")
        file_name = input()
        try:
            with open(f"{file_name}.txt", "r", encoding="UTF-8") as _:
                pass
        except Exception as _:
            print("invalid name")
        is_file_name_valid = False
    return file_name


def clean_line(line: str) -> str:
    to_replace = list("ÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛáàâãéèêíìîóòôõúùûäëïöüÄËÏÖÜ\n -ç,/Æ")
    replace_by = list("aaaaeeeiiioooouuuaaaaeeeiiioooouuuaeiouaeiou\n  c  ae")
    line = line.lower()
    for char_ro_replace, replace_by_char in zip(to_replace, replace_by):
        line = line.replace(char_ro_replace, replace_by_char)
    return line


nome = get_file_name()
letras = list("aeiouqwrtypsdfghjklzxcvbnm0123456789")
with open(f"{nome}.txt", "r", encoding="UTF-8") as markov_chain_file:
    line = markov_chain_file.readline()
    initial_letter_occurrences = [0 for _ in letras]
    letter_occurrences = [0 for _ in letras]
    word_lengths: list[list[int]] = []
    word_length_occurrences: list[list[int]] = []
    word_counts:list[int] = []
    word_stats:list[int] = []
    while line:
        line = clean_line(line)
        palavras = line[:-1].split(" ")
        while len(palavras) > len(word_counts):
            word_counts.append(len(word_counts) + 1)
            word_stats.append(0)
            word_lengths.append([])
            word_length_occurrences.append([])
        if len(palavras) in word_counts:
            word_stats[len(palavras) - 1] += 1
        for m, palavra in enumerate(palavras):
            current_word_length = word_lengths[m]
            current_occurrences = word_length_occurrences[m]
            for n, caracter in enumerate(list(palavra)):
                try:
                    if n == 0:
                        initial_letter_occurrences[letras.index(caracter)] += 1
                    else:
                        letter_occurrences[letras.index(caracter)] += 1
                except ValueError:
                    pass
            tamanho = len(palavra)
            if tamanho not in current_word_length:
                current_word_length.append(tamanho)
                current_occurrences.append(1)
            else:
                current_occurrences[current_word_length.index(tamanho)] += 1
        line = markov_chain_file.readline()
    initial_letter_frequencies = normalize_statistics(initial_letter_occurrences)
    vowel_frequencies = normalize_statistics(letter_occurrences[0:5])
    consonant_frequencies = normalize_statistics(letter_occurrences[5:])
    word_length_frequencies: list[float] = []
    for current_occurrences in word_length_occurrences:
        current_word_length_frequencies = normalize_statistics(current_occurrences)
        for word_length_frequency in current_word_length_frequencies:
            word_length_frequencies.append(word_length_frequency)
    word_frequencies = normalize_statistics(word_stats)
number = -1
while number < 0:
    print("how many words?")
    try:
        number = int(input())
    except ValueError:
        print("invalid number")
        continue
    if number < 0:
        print("invalid number")
for a in range(number):
    print(generate_word())
