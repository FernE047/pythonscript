# terminating a program using sys.exit()
import sys

while True:
    print("Type exit to exit.")
    response = input()
    if response == "exit":
        sys.exit()
    print(f"You typed {response}.")
