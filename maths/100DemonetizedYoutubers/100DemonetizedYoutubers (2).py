import random

COMPLETION_RATE_DEFAULT = 0
PARTICIPANTS_TOTAL = 100


def check_participant_guess(
    random_participants: list[int], participant_index: int
) -> bool:
    previous_guesses: list[int] = []
    for _ in range(PARTICIPANTS_TOTAL // 2):
        guess = random.randint(0, len(random_participants) - 1)
        while guess in previous_guesses:
            guess = random.randint(0, len(random_participants) - 1)
        previous_guesses.append(guess)
        if random_participants[guess] == participant_index:
            random_participants.pop(guess)
            return True
    return False


def evaluate_guess(
    individual_failure_counts: list[int], random_participants: list[int]
) -> bool:
    for participant_index in range(PARTICIPANTS_TOTAL):
        if check_participant_guess(random_participants, participant_index):
            continue
        individual_failure_counts[participant_index] += 1
        return False
    return True

def calculate_probability(number: int) -> float:
    if number == 0:
        return 0
    return number * 100 / PARTICIPANTS_TOTAL

def main() -> None:
    simulation_count = 0
    completion_rate = COMPLETION_RATE_DEFAULT
    individual_failure_counts = [0 for _ in range(PARTICIPANTS_TOTAL)]
    shuffled_participant_ids = [a for a in range(PARTICIPANTS_TOTAL)]
    random.shuffle(shuffled_participant_ids)
    for round_index in range(PARTICIPANTS_TOTAL):
        random_participants = [a for a in shuffled_participant_ids]
        is_correct_guess = evaluate_guess(
            individual_failure_counts, random_participants
        )
        if is_correct_guess:
            simulation_count += 1
            print("We have a winner !")
        completion_percentage = int(calculate_probability(round_index))
        if completion_percentage != completion_rate:
            completion_rate = completion_percentage
            print(f"{completion_rate}%")
    for participant_index, probability in enumerate(individual_failure_counts):
        if probability != 0:
            percentage = int(calculate_probability(probability))
            print(f"Participant {participant_index} : {percentage}%")
    print(f"Total : {calculate_probability(simulation_count):02d}%")


if __name__ == "__main__":
    main()
