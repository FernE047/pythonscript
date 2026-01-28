from time import time


def format_elapsed_time(seconds: float) -> str:
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
    return sign + ", ".join(parts)

def resolveBoard(
    board: tuple[list[list[bool]], tuple[int, int]],
) -> list[tuple[int, int]] | None: #TODO: implement solver
    return None

def resolveOneBoard(board: tuple[list[list[bool]], tuple[int, int]]) -> None:
    print()
    tries = 0
    begin = time()
    resolveBoard(board)
    end = time()
    print("\ntries: " + str(tries))
    duration = end - begin
    global total_time
    total_time += duration
    print("\n" + format_elapsed_time(duration) + "\n\n\n")

total_time = 0.0
for pos in (
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 2),
    (2, 3),
    (3, 3),
):
    matriz = [[False for _ in range(8)] for _ in range(8)]
    matriz[pos[0]][pos[1]] = True
    board = (matriz, pos)
    resolveOneBoard(board)
print("\n" + format_elapsed_time(total_time) + "\n\n\n")
