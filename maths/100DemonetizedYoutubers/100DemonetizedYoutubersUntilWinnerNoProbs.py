from random import shuffle
from time import time


PARTICIPANTS_TOTAL = 100
HALF_PARTICIPANTS = PARTICIPANTS_TOTAL // 2


def check_participant_failure():
    participant_numbers = [i for i in range(PARTICIPANTS_TOTAL)]
    shuffle(participant_numbers)
    for participant_index in range(HALF_PARTICIPANTS):
        if (
            participant_numbers.pop(participant_numbers.index(participant_index))
            < HALF_PARTICIPANTS
        ):
            return True
    return False


def main() -> None:
    total = 0
    start_time = time()
    try:
        while check_participant_failure():
            total += 1
    except KeyboardInterrupt:
        pass
    end_time = time()
    duration = end_time - start_time
    print(f"total : {total}")
    print(f"execution total : {duration}")
    print(f"average total :    {duration / total}")
    print(f"100k :    {(duration * 100000) / total}")
    print(f"final :    {(duration * 345484498) / total}")
    input()

    # media 100k :       0.00045348677564376093 segundos
    # Nova media 100k :  0.0003801782075167559 segundos
    # media Numpy 100k : 0.000021456736708393844 segundos

    # quantia necessaria: 345484498 no total ou
    # quantia necessaria: 1267650600228229401496703205376 no total


if __name__ == "__main__":
    main()
