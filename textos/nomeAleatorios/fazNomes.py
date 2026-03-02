from typing import Literal, overload

from numpy.random import choice

#TODO: move the probabilities to a separate file.

GenderOptions = Literal["m", "f", "n"]

MID_VOWEL_PROBABILITIES = {
    "a": 0.35697057404727445,
    "e": 0.23323685479980705,
    "i": 0.20839363241678727,
    "o": 0.123251326579836,
    "u": 0.07814761215629522,
}
MID_CONSONANTS_PROBABILITIES = {
    "b": 0.030587833219412174,
    "c": 0.035201640464798366,
    "d": 0.052973342447026665,
    "f": 0.016233766233766236,
    "g": 0.029049897470950107,
    "h": 0.07928913192071088,
    "j": 0.02665755297334245,
    "k": 0.042549555707450455,
    "l": 0.08817498291182503,
    "m": 0.06049213943950787,
    "n": 0.13841421736158582,
    "p": 0.022727272727272735,
    "q": 0.0039302802460697206,
    "r": 0.10731373889268628,
    "s": 0.09005468215994533,
    "t": 0.06766917293233084,
    "v": 0.018284347231715656,
    "w": 0.01503759398496241,
    "x": 0.0037593984962406026,
    "y": 0.05092276144907725,
    "z": 0.02067669172932331,
}
MALE_FIRST_LETTER_PROBABILITIES = {
    "a": 0.048949999999999994,
    "b": 0.037450000000000004,
    "c": 0.05985,
    "d": 0.07582,
    "e": 0.034140000000000004,
    "f": 0.01898,
    "g": 0.036680000000000004,
    "h": 0.02092,
    "i": 0.0038,
    "j": 0.15882,
    "k": 0.026160000000000003,
    "l": 0.03212,
    "m": 0.0696,
    "n": 0.01138,
    "o": 0.00417,
    "p": 0.025019999999999997,
    "q": 0.00048,
    "r": 0.10253999999999999,
    "s": 0.040780000000000004,
    "t": 0.04253,
    "u": 0.0001,
    "v": 0.006540000000000001,
    "w": 0.04216,
    "x": 0.00013,
    "y": 0.00013,
    "z": 0.10075000000000012,
}
FEMALE_FIRST_LETTER_PROBABILITIES = {
    "a": 0.06784,
    "b": 0.04605000000000001,
    "c": 0.06999,
    "d": 0.05779,
    "e": 0.04868,
    "f": 0.01252,
    "g": 0.02231,
    "h": 0.01966,
    "i": 0.00933,
    "j": 0.08178,
    "k": 0.04764,
    "l": 0.06896,
    "m": 0.11114,
    "n": 0.02147,
    "o": 0.00398,
    "p": 0.03129,
    "q": 0.00017,
    "r": 0.04157,
    "s": 0.07035,
    "t": 0.033530000000000004,
    "u": 0.0003,
    "v": 0.02015,
    "w": 0.008,
    "x": 8e-05,
    "y": 0.00391,
    "z": 0.10151000000000013,
}
NONBINARY_FIRST_LETTER_PROBABILITIES = {
    "a": 0.058570000000000004,
    "b": 0.04183,
    "c": 0.06501,
    "d": 0.06663999999999999,
    "e": 0.04154,
    "f": 0.01569,
    "g": 0.029369999999999997,
    "h": 0.02028,
    "i": 0.00661,
    "j": 0.11961000000000001,
    "k": 0.03709,
    "l": 0.05087,
    "m": 0.09074,
    "n": 0.01652,
    "o": 0.00407,
    "p": 0.028210000000000002,
    "q": 0.00032,
    "r": 0.07151,
    "s": 0.055830000000000005,
    "t": 0.03795,
    "u": 0.0002,
    "v": 0.01347,
    "w": 0.02477,
    "x": 0.0001,
    "y": 0.0020499999999999997,
    "z": 0.10115000000000003,
}
NAME_LENGTH_PROBABILITIES = {
    3: 0.0248,
    4: 0.0908,
    5: 0.2184,
    6: 0.26030000000000003,
    7: 0.20440000000000003,
    8: 0.12140000000000001,
    9: 0.0557,
    10: 0.024199999999999878,
}
FULL_NAME_LENGTH_PROBABILITIES = {
    2: 0.45,
    3: 0.45,
    4: 0.1,
}
GENDERS: tuple[GenderOptions, ...] = ("m", "f", "n")
GENDER_NAMES = ("Masculine", "Feminine", "Non-Binary")
DOUBLE_CONSONANTS_CASES = ("b", "c", "d", "f", "g", "k", "p", "t", "v")
DOUBLE_CONSONANTS_PROBABILITY = 0.05
DOUBLE_CONSONANTS = ("l", "r", "h")
VOWEL_PARITY = 2  # after a consonant block, there's a vowel
END_SYLLABLE_CONSONANTS = ("l", "s", "r", "y", "w", "z", "x", "n", "m")
END_SYLLABLE_CONSONANTS_PROBABILITY = 0.25
NON_DOUBLE_CONSONANTS = ("h", "j")
VOWELS = tuple(MID_VOWEL_PROBABILITIES.keys())


@overload
def choose_random_from_dict(dictionary: dict[int, float]) -> int: ...


@overload
def choose_random_from_dict(dictionary: dict[str, float]) -> str: ...


def choose_random_from_dict(
    dictionary: dict[str, float] | dict[int, float],
) -> str | int:
    keys = list(dictionary.keys())
    probabilities = list(dictionary.values())
    return choice(keys, 1, p=probabilities)[0]  # type: ignore


def generate_middle_vowel() -> str:
    return choose_random_from_dict(MID_VOWEL_PROBABILITIES)


def generate_middle_consonant() -> str:
    return choose_random_from_dict(MID_CONSONANTS_PROBABILITIES)


def generate_initial_char(gender: GenderOptions = "n") -> str:
    next_char = ""
    probability = NONBINARY_FIRST_LETTER_PROBABILITIES
    if gender == "m":
        probability = MALE_FIRST_LETTER_PROBABILITIES
    elif gender == "f":
        probability = FEMALE_FIRST_LETTER_PROBABILITIES
    initial_char = choose_random_from_dict(probability)
    if initial_char == "q":
        next_char = "u"
    if initial_char in DOUBLE_CONSONANTS_CASES:
        is_double_consonant = random_bool(DOUBLE_CONSONANTS_PROBABILITY)
        if is_double_consonant:
            next_char = generate_middle_consonant()
            while next_char not in DOUBLE_CONSONANTS:
                next_char = generate_middle_consonant()
    return initial_char + next_char


def random_bool(probability: float) -> bool:
    return choice([False, True], 1, p=[1 - probability, probability])[0]


def generate_end(length: int, starts_with_vowel: bool = True) -> str:
    end_part = ""
    double_consonant_flag = False
    was_previous_vowel = starts_with_vowel
    for index in range(length):
        if bool(index % VOWEL_PARITY) == was_previous_vowel:
            end_part += generate_middle_vowel()
            double_consonant_flag = False
            continue
        current_char = generate_middle_consonant()
        if current_char == "q":
            end_part += "qu"
            continue
        end_part += current_char
        if current_char in END_SYLLABLE_CONSONANTS:
            if double_consonant_flag:
                continue
            double_consonant_flag = random_bool(END_SYLLABLE_CONSONANTS_PROBABILITY)
            if double_consonant_flag:
                # next one must be a consonant.
                was_previous_vowel = not was_previous_vowel
            continue
        if current_char in NON_DOUBLE_CONSONANTS:
            continue
        double_consonant_flag = random_bool(DOUBLE_CONSONANTS_PROBABILITY)
        if double_consonant_flag:
            current_char = generate_middle_consonant()
            while current_char not in DOUBLE_CONSONANTS:
                current_char = generate_middle_consonant()
            end_part += current_char
    return end_part


def generate_name(gender: GenderOptions = "n") -> str:
    length = choose_random_from_dict(NAME_LENGTH_PROBABILITIES)
    begin = generate_initial_char(gender=gender)
    starts_with_vowel = begin[0] in VOWELS
    end = generate_end(length - 1, starts_with_vowel=starts_with_vowel)
    return begin + end


def generate_full_name(gender: GenderOptions = "n") -> str:
    name_size = choose_random_from_dict(NAME_LENGTH_PROBABILITIES)
    name_list = [generate_name(gender)]
    for _ in range(name_size - 1):
        name_list.append(generate_name())
    full_name = " ".join(name_list)
    return full_name


def main() -> None:
    for gender, gender_name in zip(GENDERS, GENDER_NAMES):
        print(f"\n{gender_name}:")
        for name_index in range(100):
            print(f"{name_index:02d} : {generate_full_name(gender)}")


if __name__ == "__main__":
    main()
