from numpy.random import shuffle
from time import time

# Last Excecution Data :

# average 100k :       0.00045348677564376093 seconds
# new average 100k :  0.0003801782075167559 seconds
# average Numpy 100k : 0.000021456736708393844 seconds

# required amount: 345484498 in total or
# required amount: 1267650600228229401496703205376 in total


def check_failure_attempt() -> bool:
    participant_numbers = [number for number in range(100)]
    shuffle(participant_numbers)
    for participante in range(50):
        if participant_numbers.pop(participant_numbers.index(participante)) < 50:
            return True
    return False


def main() -> None:
    attempt_count = 0
    start_time = time()
    try:
        while check_failure_attempt():
            attempt_count += 1
    except KeyboardInterrupt:
        pass
    end_time = time()
    execution_duration = end_time - start_time
    print(f"total : {attempt_count}")
    print(f"total execution : {execution_duration}")
    print(f"total average :    {execution_duration / attempt_count}")
    print(f"100k :    {(execution_duration * 100000) / attempt_count}")
    print(f"final :    {(execution_duration * 345484498) / attempt_count}")
    input("press enter to exit")


if __name__ == "__main__":
    main()
