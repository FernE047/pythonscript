from time import time
from typing import Callable
from clean_directory import clean_project_folder
from generate_config import generate_config
from recolor_frames import recolor_frames
from morph import morph
from correct_frames import correct_frames
from generate_gif import generate_gif

# esse algoritmo faz o morph completo

EXECUTABLE = "python"
STEPS = (
    (clean_project_folder, "clean directory"),
    (generate_config, "make configurations"),
    (recolor_frames, "recolor"),
    (morph, "make animations"),
    (correct_frames, "frame correction"),
    (generate_gif, "make Gif"),
)


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


def execute_process(command: Callable[[], None], name: str) -> None:
    print(f"starting {name}")
    start_time = time()
    command()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"\n{name} finished")
    print_elapsed_time(elapsed_time)


def main() -> None:
    while True:
        start_time = time()
        for command, name in STEPS:
            execute_process(command, name)
        print("\nfinished")
        end_time = time()
        elapsed_time = end_time - start_time
        print_elapsed_time(elapsed_time)


if __name__ == "__main__":
    main()
