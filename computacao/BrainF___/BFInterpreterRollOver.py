class Config:
    def __init__(self, debug: bool = False, debug_final: bool = False) -> None:
        self.debug = debug
        self.debug_final = debug_final
        self.steps = 0
        self.isOut = 2

    def update_debug(self, program_script: str) -> None:
        if program_script == "DEBUG ON":
            self.debug = True
            self.debug_final = True
            print("DEBUG ACTIVATED")
            return
        if program_script == "DEBUG OFF":
            self.debug = False
            self.debug_final = False
            print("DEBUG DESACTIVATED")
            return
        if program_script == "DEBUG FINAL ON":
            self.debug_final = True
            print("DEBUG FINAL ACTIVATED")
            return
        if program_script == "DEBUG FINAL OFF":
            self.debug_final = False
            print("DEBUG FINAL DESACTIVATED")
            return


def count_open_bracket(program_script: str) -> int:
    open_bracket_count = 0
    for char in program_script:
        if char == "[":
            open_bracket_count += 1
            continue
        if char == "]":
            open_bracket_count -= 1
            continue
    return open_bracket_count


def find_end_of_loop(program_script: str, read_index: int) -> int:
    open_bracket_count = 0
    while True:
        read_index += 1
        try:
            char = program_script[read_index]
        except IndexError:
            return read_index
        if char == "[":
            open_bracket_count += 1
        if char == "]":
            if open_bracket_count == 0:
                return read_index
            open_bracket_count -= 1


def increment_and_wrap(current_value: int) -> int:
    if current_value == 255:
        return 0
    return current_value + 1


def decrement_and_wrap(current_value: int) -> int:
    if current_value == 0:
        return 255
    return current_value - 1


def execute_script(
    program_script: str,
    memory_tape: list[int],
    config: Config,
    read_index: int = 0,
    cursor: int = 0,
) -> tuple[int, int] | list[int]:
    while True:
        char = program_script[read_index]
        if config.debug_final:
            config.steps += 1
        if config.debug:
            print(char, end=" ")
        if char == "+":
            memory_tape[cursor] = increment_and_wrap(memory_tape[cursor])
        elif char == "-":
            memory_tape[cursor] = decrement_and_wrap(memory_tape[cursor])
        elif char == ">":
            cursor += 1
            if cursor >= len(memory_tape):
                memory_tape.append(0)
        elif char == "<":
            if cursor == 0:
                memory_tape = [0] + memory_tape
            else:
                cursor -= 1
        elif char == ",":
            config.isOut = 0
            memory_tape[cursor] = int(input("\ninput:"))
        elif char == ".":
            if config.isOut == 2:
                config.isOut = 1
                print(f"output: {memory_tape[cursor]}", end="")
            elif config.isOut == 1:
                print(f" {memory_tape[cursor]}", end="")
            else:
                config.isOut = 1
                print(f"\noutput: {memory_tape[cursor]}", end="")
        elif char == "[":
            if config.debug:
                print("")
            if memory_tape[cursor]:
                leituraInicial = read_index + 1
                while memory_tape[cursor]:
                    cursor, read_index = execute_script(
                        program_script, memory_tape, config, leituraInicial, cursor
                    )
            else:
                read_index = find_end_of_loop(program_script, read_index)
        elif char == "]":
            if config.debug:
                print("]")
            return (cursor, read_index)
        read_index += 1
        if config.debug:
            print(f"{cursor} {memory_tape}")
        if read_index == len(program_script):
            break
    print("")
    return memory_tape


def main() -> None:
    config = Config()
    while True:
        print("enter the brainfuck program")
        programa = input()
        if programa == "0":
            break
        if programa.find("DEBUG") != -1:
            config.update_debug(programa)
            continue
        open_bracket_count = count_open_bracket(programa)
        if open_bracket_count == 0:
            memory_tape = execute_script(programa, [0], config)
            if config.debug_final:
                print("")
                print(programa)
                print(memory_tape)
                print(f"steps: {config.steps}")
            continue
        if open_bracket_count < 0:
            print(f"missing {-open_bracket_count} bracket: [")
            continue
        print(f"missing {open_bracket_count} bracket: ]")


if __name__ == "__main__":
    main()
