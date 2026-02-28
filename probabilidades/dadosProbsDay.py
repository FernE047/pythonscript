# calculate the probability of rolling the same number on a certain amount of dice and how long it would take to get that result if you rolled one die every second
# prints the amount of centuries, years, days, hours, minutes, seconds

ROLLS_PER_SECOND = 1
MAX_DICES = 20
DICE_FACES = 6

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365
YEARS_PER_CENTURY = 100


def carry(current: int, conversion: int) -> tuple[int, int]:
    return current % conversion, current // conversion


def main() -> None:
    for dice_count in range(MAX_DICES):
        print(f"\nDices: {dice_count + 1}")
        denom = DICE_FACES**dice_count

        total_seconds = denom // ROLLS_PER_SECOND

        seconds = total_seconds
        seconds, minutes = carry(seconds, SECONDS_PER_MINUTE)
        minutes, hours = carry(minutes, MINUTES_PER_HOUR)
        hours, days = carry(hours, HOURS_PER_DAY)
        days, years = carry(days, DAYS_PER_YEAR)
        years, centuries = carry(years, YEARS_PER_CENTURY)

        print(f"centuries: {centuries}")
        print(f"years: {years}")
        print(f"days: {days}")
        print(f"hours: {hours}")
        print(f"minutes: {minutes}")
        print(f"seconds: {seconds}")
        print(f"probability: 1 in {denom}")


if __name__ == "__main__":
    main()