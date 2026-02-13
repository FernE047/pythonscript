from typing import cast


class Config:
    def __init__(self):
        self.debug = False
        self.debug_final = False
        self.limit_exec = 10**4
        self.limit_value = self.limit_exec
        self.limit_steps = 0
        self.isOut = 2
        self.steps = 0

    def update_debug(self, program_script: str) -> None:
        if program_script == "config.debug ON":
            self.debug = True
            self.debug_final = True
            print("config.debug ACTIVATED")
            return
        if program_script == "config.debug OFF":
            self.debug = False
            self.debug_final = False
            print("config.debug DESACTIVATED")
            return
        if program_script == "config.debug FINAL ON":
            self.debug_final = True
            print("config.debug FINAL ACTIVATED")
            return
        if program_script == "config.debug FINAL OFF":
            self.debug_final = False
            print("config.debug FINAL DESACTIVATED")
            return
        if program_script.find("config.debug LIMIT STEPS ") != -1:
            self.limit_steps = int(program_script[20:])
            print(f"config.limit_steps={self.limit_steps}")
            print("config.debug FINAL ACTIVATED")
            self.debug_final = True
            return
        if program_script.find("config.debug LIMIT VALUE ") != -1:
            self.limit_value = int(program_script[19:])
            print(f"config.limit_value={self.limit_value}")
            return
        if program_script.find("config.debug LIMIT ") != -1:
            self.limit_exec = int(program_script[13:])
            print(f"config.limit_exec={self.limit_exec}")
            return
        if program_script.find("config.debug LIMITES ") != -1:
            limits = int(program_script[14:])
            self.limit_exec = limits
            self.limit_steps = limits
            self.limit_value = limits
            print(f"config.limit_exec={self.limit_exec}")
            print(f"config.limit_value={self.limit_value}")
            print(f"config.limit_steps={self.limit_steps}")
            print("config.debug FINAL ACTIVATED")
            self.debug_final = True
            return


def count_brackets(program_script: str) -> int:
    loop = 0
    for char in program_script:
        if char == "[":
            loop += 1
        elif char == "]":
            loop -= 1
    return loop


def findLoopEnd(program_script: str, read_index: int) -> int:
    open_bracket_count = 0
    while True:
        read_index += 1
        current_character = program_script[read_index]
        if current_character == "[":
            open_bracket_count += 1
        if current_character == "]":
            if open_bracket_count == 0:
                break
            else:
                open_bracket_count -= 1
    return read_index


def execute_program(
    program_script: str,
    memory_tape: list[int],
    config: Config,
    read_index: int = 0,
    cursor: int = 0,
) -> list[int] | tuple[int, int, list[int]]:
    is_giving_error = False
    while True:
        current_instruction = program_script[read_index]
        if config.debug_final:
            config.steps += 1
        if config.debug:
            print(current_instruction, end=" ")
        if current_instruction == "+":
            memory_tape[cursor] += 1
        elif current_instruction == "-":
            memory_tape[cursor] -= 1
        elif current_instruction == ">":
            cursor += 1
            if cursor >= len(memory_tape):
                memory_tape.append(0)
        elif current_instruction == "<":
            if cursor == 0:
                memory_tape = [0] + memory_tape
            else:
                cursor -= 1
        elif current_instruction == ",":
            config.isOut = 0
            memory_tape[cursor] = int(input("\nentrada:"))
        elif current_instruction == ".":
            if config.isOut == 2:
                config.isOut = 1
                print(f"saida:{memory_tape[cursor]}", end="")
            elif config.isOut == 1:
                print(f" {memory_tape[cursor]}", end="")
            else:
                config.isOut = 1
                print(f"\nsaida:{memory_tape[cursor]}", end="")
        elif current_instruction == "[":
            if config.debug:
                print("")
            if memory_tape[cursor]:
                initial_read_index = read_index + 1
                try:
                    while memory_tape[cursor]:
                        cursor, read_index, memory_tape = cast(
                            tuple[int, int, list[int]],
                            execute_program(
                                program_script,
                                memory_tape,
                                config,
                                initial_read_index,
                                cursor,
                            ),
                        )
                except IndexError:
                    print("Erro")
                    is_giving_error = True
            else:
                read_index = findLoopEnd(program_script, read_index)
        elif current_instruction == "]":
            return (cursor, read_index, memory_tape)
        if len(memory_tape) >= config.limit_exec:
            if not (is_giving_error):
                print("limite de execução")
            break
        if (memory_tape[cursor] >= config.limit_value) or (
            memory_tape[cursor] <= -config.limit_value
        ):
            if not (is_giving_error):
                print(f"limite de valor excedido pelo indice:{cursor}")
                print(f"valor:{memory_tape[cursor]}")
            break
        if config.debug_final:
            if config.limit_steps > 0:
                if config.steps >= config.limit_steps:
                    if not (is_giving_error):
                        print("limite de passos")
                    break
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
        config.isOut = 2
        config.steps = 0
        print("escreva o programa")
        program_script = input()
        if program_script.find("config.debug") != -1:
            config.update_debug(program_script)
            continue
        if program_script == "0":
            break
        open_bracket_count = count_brackets(program_script)
        memory_tape = [0]
        if open_bracket_count < 0:
            print(f"falta {-open_bracket_count} colchete: [")
            continue
        if open_bracket_count > 0:
            print(f"falta {open_bracket_count} colchete: ]")
            continue
        memory_tape = cast(
            list[int], execute_program(program_script, memory_tape, config)
        )
        if config.debug_final:
            print("")
            print(program_script)
            print(memory_tape)
            print(f"steps: {config.steps}")


if __name__ == "__main__":
    main()
