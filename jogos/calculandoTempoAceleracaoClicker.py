# this script calculates the time it takes to produce a certain amount of products in the game "Cookie Clicker" based on the number of producers, production rate, and cost of production.
PRODUCER_COUNT = 1
PRODUCTION_RATE_PER_MIN = 0.001
PRODUCTION_COST = 1000


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


def calculate_production_time(
    producer_count: int,
    production_rate_per_min: float,
    production_cost: float,
    production_needed: float,
) -> float:
    output_per_second = production_rate_per_min * producer_count / 60
    elapsed_time = 0.0
    while output_per_second < production_needed:
        current_time = production_cost / output_per_second
        elapsed_time += current_time
        producer_count += 1
        output_per_second = production_rate_per_min * producer_count / 60
    return elapsed_time


def calculate_factory_delay(
    producer_count: int,
    production_rate_per_min: float,
    production_cost: float,
    production_needed: float,
) -> float:
    output_per_second = production_rate_per_min * producer_count / 60
    elapsed_time = 0.0
    while producer_count < production_needed:
        current_time = production_cost / output_per_second
        elapsed_time += current_time
        producer_count += 1
        output_per_second = production_rate_per_min * producer_count / 60
    return elapsed_time


def calculate_product_delay(
    producer_count: int,
    production_rate_per_min: float,
    production_cost: float,
    production_needed: float,
) -> float:
    output_per_second = production_rate_per_min * producer_count / 60
    product = 0.0
    elapsed_time = 0.0
    while product < production_needed:
        current_time = production_cost / output_per_second
        elapsed_time += current_time
        product += production_cost
        producer_count += 1
        output_per_second = production_rate_per_min * producer_count / 60
    return elapsed_time


def main() -> None:
    tempo = calculate_production_time(
        PRODUCER_COUNT, PRODUCTION_RATE_PER_MIN, PRODUCTION_COST, PRODUCTION_COST * 10
    )
    print(f"\nPRODUCER_COUNT : {PRODUCER_COUNT}\n")
    print_elapsed_time(tempo)


if __name__ == "__main__":
    main()
