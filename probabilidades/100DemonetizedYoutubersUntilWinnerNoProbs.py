from random import sample
from time import time

# Last Excecution Data :

# average 100k : 0.00045391589059292357 segundos

def attempt_failure() -> bool:
    for participant_index in range(51):
        if participant_index not in sample(range(participant_index, 100), 50):
            return True
    return False


def main() -> None:
    attempt_count = 0
    start_time = time()
    try:
        while attempt_failure():
            attempt_count += 1
    except KeyboardInterrupt:
        pass
    end_time = time()
    execution_duration = end_time - start_time
    print(f"total : {attempt_count}")
    print(f"total execution : {execution_duration}")
    print(f"total average :    {execution_duration / attempt_count}")
    print(f"100k :    {(execution_duration * 100000) / attempt_count}")
    input("press enter to exit")


if __name__ == "__main__":
    main()
