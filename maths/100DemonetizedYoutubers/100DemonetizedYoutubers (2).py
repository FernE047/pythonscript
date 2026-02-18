import random


def main() -> None:
    simulation_count = 0
    participants_total = 100
    completion_rate = 0
    individual_failure_counts = [0 for _ in range(participants_total)]
    shuffled_participant_ids = [a for a in range(participants_total)]
    random.shuffle(shuffled_participant_ids)
    for round_index in range(participants_total):
        random_participants = [a for a in shuffled_participant_ids]
        is_correct_guess = False
        for participant_index in range(participants_total):
            is_correct_guess = False
            previous_guesses: list[int] = []
            for _ in range(participants_total // 2):
                guess = random.randint(0, len(random_participants) - 1)
                while guess in previous_guesses:
                    guess = random.randint(0, len(random_participants) - 1)
                previous_guesses.append(guess)
                if random_participants[guess] == participant_index:
                    is_correct_guess = True
                    random_participants.pop(guess)
                    break
            if not (is_correct_guess):
                individual_failure_counts[participant_index] += 1
                break
        if is_correct_guess:
            simulation_count += 1
            print("temos um ganhador")
        porcentagemAtual = int(round_index * 100 / participants_total)
        if porcentagemAtual != completion_rate:
            completion_rate = porcentagemAtual
            print(f"{completion_rate}%")
    for participant_index, prob in enumerate(individual_failure_counts):
        if prob != 0:
            print(f"participante {participant_index} : {prob * 100 / participants_total}%")
    print(f"total : {simulation_count * 100 / participants_total}%")


if __name__ == "__main__":
    main()
