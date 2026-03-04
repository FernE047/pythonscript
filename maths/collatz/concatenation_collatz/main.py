def concatenation_collatz(j: int) -> int:
    if j % 2 == 1:
        return int(str(j) * 2) + 1
    return int(j // 2)



def main() -> None:
    previous_numbers: list[int] = []
    print("this program will print the collatz sequence of a number but instead of multiplying by 3 and adding 1, it will concatenate the number with itself and add 1")
    print("even numbers are divided by 2")
    print("until it reaches 1")
    print("enter the seed number")
    current_number = int(input())
    print("enter 1 to print all numbers")
    should_print_all = input()
    print(str(current_number))
    while current_number != 1:
        current_number = concatenation_collatz(current_number)
        if should_print_all == "1":
            print(str(current_number))
        if current_number % 2:
            if should_print_all != "1":
                print(str(current_number))
            if current_number in previous_numbers:
                break
            previous_numbers.append(current_number)
    if current_number == 1:
        print("expected end")
    else:
        print("repeated number, expected end")


if __name__ == "__main__":
    main()
