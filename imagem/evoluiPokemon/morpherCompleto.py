import subprocess
import gc
from time import time

# esse algoritmo faz o morph completo


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
    print(sign + ", ".join(parts))


def fazProcesso(processo:str, nome: str) -> None:
    print(f"starting {nome}")
    start_time = time()
    subprocess.call(processo)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"\n{nome} finished")
    print_elapsed_time(elapsed_time)


def main() -> None:
    while True:
        start_time = time()
        fazProcesso(
            "python ./preparaMorph.py ",
            "clean directory",
        )
        fazProcesso(
            "python ./analisaEFazConfig.py ",
            "make configurations",
        )
        fazProcesso("python ./recolor.py ", "recolor")
        fazProcesso("python ./morpher.py ", "make animations")
        fazProcesso(
            "python ./corrigeFrames.py ",
            "frame correction",
        )
        fazProcesso("python ./fazGif.py ", "make Gif")
        print("\nfinished")
        end_time = time()
        elapsed_time = end_time - start_time    
        print_elapsed_time(elapsed_time)
        gc.collect()


if __name__ == "__main__":
    main()
