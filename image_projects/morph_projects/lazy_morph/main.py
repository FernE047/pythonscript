from time import time
from typing import Callable
from clean_directory import clean_project_folder
from generate_config import generate_config
from recolor_frames import recolor_frames
from morph import morph
from correct_frames import correct_frames
from generate_gif import generate_gif
from datetime import timedelta

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


def execute_process(command: Callable[[], None], name: str) -> None:
    print(f"starting {name}")
    start_time = time()
    command()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"\n{name} finished")
    elapsed_time_str = str(timedelta(seconds=elapsed_time))
    print(f"Elapsed time: {elapsed_time_str}")


def main() -> None:
    while True:
        start_time = time()
        for command, name in STEPS:
            execute_process(command, name)
        print("\nfinished")
        end_time = time()
        elapsed_time = end_time - start_time
        elapsed_time_str = str(timedelta(seconds=elapsed_time))
        print(f"Elapsed time: {elapsed_time_str}")


if __name__ == "__main__":
    main()
