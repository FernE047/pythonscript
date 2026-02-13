from typing import cast


class Config:
    # this code used to have a lot of global variables, now they are encapsulated in this class
    # but they are mutable so they would'nt work as constants
    def __init__(self) -> None:
        self.debug = False
        self.debug_final = False
        self.limit_exec = 10000
        self.limit_value = 10000
        self.limit_steps = 10000
        self.steps = 0
        self.enable_print = False
        self.is_giving_error = False
        self.valid_script_count = 0
        self.script_id = 0


def generate_bf_code(info: tuple[int, int]) -> str:
    available_chars = ["+", "-", "<", ">", "[", "]"]
    id_script, size = info
    brainfuck_instructions: list[str] = []
    while id_script > 5:
        char = id_script % 6
        id_script = id_script // 6
        brainfuck_instructions.append(available_chars[char])
    brainfuck_instructions.append(available_chars[id_script])
    while len(brainfuck_instructions) < size:
        brainfuck_instructions.append(available_chars[0])
    program_script = "".join(brainfuck_instructions)
    return program_script


def generate_code(config: Config) -> str:
    id_official = convert_id(config.script_id)
    program_script = generate_bf_code(id_official)
    return program_script


def convert_id(number: int) -> tuple[int, int]:
    size = 1
    heuristic_value = 0
    official_id = 0
    while True:
        total = 6**size
        heuristic_value += total
        if number < heuristic_value:
            return (number - official_id, size)
        official_id += total
        size += 1


def display_results(result_dictionary: dict[int, str], config: Config) -> None:
    print("")
    for key_number in range(min(result_dictionary), max(result_dictionary) + 1):
        if key_number in result_dictionary.keys():
            print(config.valid_script_count, end="/")
            print(config.script_id, end="\t")
            print(key_number, end="\t")
            print(result_dictionary[key_number])


def check_bracket_balance(program_script: str) -> int:
    open_bracket_count = 0
    for char in program_script:
        if char == "[":
            open_bracket_count += 1
            continue
        if char == "]":
            if open_bracket_count == 0:
                return -1
            open_bracket_count -= 1
    return open_bracket_count


def find_closing_bracket(program_script: str, read_index: int) -> int:
    open_bracket_count = 0
    while True:
        read_index += 1
        char = program_script[read_index]
        if char == "[":
            open_bracket_count += 1
            continue
        if char == "]":
            if open_bracket_count == 0:
                return read_index
            open_bracket_count -= 1


def test_errors(memory_tape: list[int], cursor: int, config: Config) -> bool:
    try:
        if len(memory_tape) >= config.limit_exec:
            if not config.is_giving_error:
                if config.enable_print:
                    print("execution limit exceeded", end="\t")
            return True
        if (memory_tape[cursor] >= config.limit_value) or (
            memory_tape[cursor] <= -config.limit_value
        ):
            if not config.is_giving_error:
                if config.enable_print:
                    print(
                        f"value limit exceeded at index {cursor} : {memory_tape[cursor]}",
                        end="\t",
                    )
            return True
        if config.limit_steps > 0:
            if config.steps >= config.limit_steps:
                if not config.is_giving_error:
                    if config.enable_print:
                        print("step limit exceeded", end="\t")
                return True
    except Exception as _:
        print("memory access error", end="\t")
        return True
    return False


def execute_bf(
    program_script: str,
    memory_tape: tuple[int, int, list[int]] | list[int],
    config: Config,
    read_index: int = 0,
    cursor: int = 0,
) -> tuple[int, int, list[int]] | list[int]:
    assert isinstance(memory_tape, list)
    config.is_giving_error = False
    while True:
        if test_errors(memory_tape, cursor, config):
            break
        char = program_script[read_index]
        if config.debug_final:
            config.steps += 1
        if char == "+":
            memory_tape[cursor] += 1
        elif char == "-":
            memory_tape[cursor] -= 1
        elif char == ">":
            cursor += 1
            if cursor >= len(memory_tape):
                memory_tape.append(0)
        elif char == "<":
            if cursor == 0:
                memory_tape = [0] + memory_tape
            else:
                cursor -= 1
        elif char == "[":
            if memory_tape[cursor]:
                leituraInicial = read_index + 1
                try:
                    while memory_tape[cursor]:
                        cursor, read_index, memory_tape = cast(
                            tuple[int, int, list[int]],
                            execute_bf(
                                program_script,
                                memory_tape,
                                config,
                                leituraInicial,
                                cursor,
                            ),
                        )
                except Exception as _:
                    config.is_giving_error = True
            else:
                read_index = find_closing_bracket(program_script, read_index)
        elif char == "]":
            return (cursor, read_index, memory_tape)
        read_index += 1
        if test_errors(memory_tape, cursor, config):
            break
        if read_index == len(program_script):
            break
    return memory_tape


def main() -> None:
    config = Config()
    found_results: list[int] = []
    optimal_step_count: dict[int, str] = {}
    potLimite = 10
    while config.valid_script_count <= 10**potLimite:
        config.steps = 0
        programa = generate_code(config)
        quantiaColcheteAberto = check_bracket_balance(programa)
        if quantiaColcheteAberto == 0:
            memory_tape: tuple[int, int, list[int]] | list[int] = [0]
            memory_tape = execute_bf(programa, memory_tape, config)
            if config.enable_print:
                print(config.valid_script_count, end="/")
                print(config.script_id, end="\t")
                print(programa, end="\t")
                print(memory_tape, end="\t")
                print(f"passos: {config.steps}")
            if isinstance(memory_tape, list):
                for result_output in memory_tape:
                    if config.steps == config.limit_exec:
                        break
                    if result_output not in found_results:
                        found_results.append(result_output)
                        optimal_step_count[result_output] = programa
            config.valid_script_count += 1
        config.script_id += 1
        if config.script_id % (7 * 10 ** (potLimite - 2)) == 0:
            display_results(optimal_step_count, config)
    for _ in range(min(optimal_step_count), max(optimal_step_count) + 1):
        display_results(optimal_step_count, config)


if __name__ == "__main__":
    main()
