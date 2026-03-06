from datetime import timedelta

# this script calculates the time it takes to produce a certain amount of products in the game "Cookie Clicker" based on the number of producers, production rate, and cost of production.
PRODUCER_COUNT = 1
PRODUCTION_RATE_PER_MIN = 0.001
PRODUCTION_COST = 1000


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
    elapsed_time = calculate_production_time(
        PRODUCER_COUNT, PRODUCTION_RATE_PER_MIN, PRODUCTION_COST, PRODUCTION_COST * 10
    )
    print(f"\nPRODUCER_COUNT : {PRODUCER_COUNT}\n")
    elapsed_time_str = str(timedelta(seconds=elapsed_time))
    print(f"Elapsed time: {elapsed_time_str}")


if __name__ == "__main__":
    main()
