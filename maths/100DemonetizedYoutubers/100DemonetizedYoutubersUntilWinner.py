import random
from time import time

# code results:

# media total :    0.0005307446075174813 segundos
# expectativa 100k : 53.07446075174813 segundos


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


def print_data(individual_failure_counts: list[int], total: int) -> None:
    print(f"\ntotal : {total}\n\ncoletivo")
    for participant, failure_probability in enumerate(individual_failure_counts):
        print(f"participant {participant} : {failure_probability * 100 / total:.20f}%")
    print("\nindividual")
    for participant, quant in enumerate(individual_failure_counts):
        print(f"participant {participant} : {quant}")
    print()
    print(f"total : {total}")
    print()


PARTICIPANTS_TOTAL = 100
HALF_PARTICIPANTS = PARTICIPANTS_TOTAL // 2


def main() -> None:
    simulation_count = 0
    individual_failure_counts = [0 for _ in range(PARTICIPANTS_TOTAL)]
    start_time = time()
    try:
        while True:
            simulation_count += 1
            ehCerto = evaluate_guess(individual_failure_counts)
            if ehCerto:
                print("We have a winner !")
                break
    except KeyboardInterrupt:
        pass
    end_time = time()
    print_data(individual_failure_counts, simulation_count)
    duration = end_time - start_time
    print("total execution time : ")
    print_elapsed_time(duration)
    print("average time :    ")
    print_elapsed_time(duration / simulation_count)
    print("expected time for 100k : ")
    print_elapsed_time((duration / simulation_count) * 100000)


def evaluate_guess(individual_failure_counts: list[int]) -> bool:
    for participant in range(PARTICIPANTS_TOTAL):
        if check_participant_guess(participant):
            continue
        individual_failure_counts[participant] += 1
        return False
    return True


def check_participant_guess(participant: int) -> bool:
    selected_guesses = random.sample(
        range(participant, PARTICIPANTS_TOTAL), HALF_PARTICIPANTS
    )
    for tentativa in range(HALF_PARTICIPANTS):
        guess = selected_guesses[tentativa]
        if guess == participant:
            return True
    return False


if __name__ == "__main__":
    main()
