from typing import Literal

# this code was supposed to be a 4D to 2D projection, but it is currently only a 4D coordinates parser, that can be used for the projection later on

TOTAL_DIMENSIONS = 4
NOT_FOUND = -1
EXIT_COMMAND = "exit"


def ehNumero(texto: str) -> bool:
    return texto.isnumeric()


def parseCoordinates(coord_txt: str) -> tuple[int, ...] | Literal[False]:
    if not coord_txt:
        return False
    if coord_txt.find(",") == NOT_FOUND:
        return False
    elements = coord_txt.split(",")
    if len(elements) != TOTAL_DIMENSIONS:
        return False
    for element in elements:
        if not element.isnumeric():
            return False
    return tuple(int(element) for element in elements)


def main() -> None:
    coordinates_list: list[tuple[int, ...]] = []
    while True:
        user_input = input()
        if user_input.lower() == EXIT_COMMAND:
            break
        coordinate = parseCoordinates(user_input)
        if coordinate:
            coordinates_list.append(coordinate)
        print(coordinates_list)


if __name__ == "__main__":
    main()
