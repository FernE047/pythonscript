from pathlib import Path

from structures import load_collatz
from structures import Collatz_Function
from structures import Rule
from time import time
from datetime import timedelta


def main() -> None:
    from_collatz = 5  # min=2
    to_collatz = 6
    next_collatz = load_collatz(from_collatz)
    execution_times: list[float] = []
    for collatz_level in range(from_collatz, to_collatz):
        start_time = time()
        current_collatz = next_collatz
        next_collatz = Collatz_Function()
        text_proof = f"{current_collatz}\n"
        core_rules = current_collatz.get_rules(["core"])
        generative_rules = current_collatz.get_rules(["generative"])
        passive_rules = current_collatz.get_rules(["passive"])
        for rule in passive_rules:
            next_collatz.append_rule(rule.copy())
        for rule in core_rules:
            new_rule = rule.copy()
            new_rule.set_equation_type("passive")
            next_collatz.append_rule(new_rule)
        for rule_1 in generative_rules:
            for rule_2 in current_collatz.get_structural_function().get_rules():
                text_proof += "passo 1 :\n\n\n"
                new_proof_part, new_formato = rule_1.solve(rule_2, text_proof)
                text_proof += f"{new_proof_part}\n"
                if new_formato is None:
                    continue
                new_formula = rule_1.get_equation().copy()
                if rule_2.get_equation_type() == "generative":
                    new_rule = Rule(new_formato, new_formula, "generative")
                    next_collatz.append_rule(new_rule)
                    continue
                for rule_3 in generative_rules:
                    text_proof = f"\n{rule_1}\n{rule_2}\n{rule_3}\n"
                    formula_1 = rule_1.get_equation().copy()
                    formula_2 = rule_2.get_equation().copy()
                    formula_3 = rule_3.get_equation().inverse_expression().copy()
                    text_proof += f"{formula_1}\n{formula_2}\n{formula_3}\n"
                    formula_4 = formula_3.combine_expressions(
                        formula_2.combine_expressions(formula_1)
                    )
                    text_proof += f"{formula_4}\n"
                    target_format = rule_3.get_modulus_rule()
                    text_proof += f"{formula_4}\n{new_formato}\n{target_format}\n"
                    new_proof_part_2, new_formato_2 = new_formato.solve(
                        target_format, formula_4, text_proof
                    )
                    text_proof += f"teste : {new_proof_part_2}\n"
                    if new_formato_2 is None:
                        continue
                    new_rule = Rule(new_formato_2, formula_4, "core")
                    next_collatz.append_rule(new_rule)
        filename = Path(f"collatz{collatz_level}de{collatz_level + 1}.txt")
        with open(filename, "w", encoding="utf-8") as proof_file:
            proof_file.write(text_proof)
        end_time = time()
        print(f"collatz {collatz_level + 1} : ")
        print(next_collatz)
        next_collatz.save_collatz_rules(collatz_level + 1)
        execution_times.append(end_time - start_time)
        elapsed_time_str = str(timedelta(seconds=execution_times[-1]))
        print(f"Elapsed time: {elapsed_time_str}")
        print("\n")
    if len(execution_times) > 1:
        print("total : ")
        total_elapsed_time_str = str(timedelta(seconds=sum(execution_times)))
        print(f"Elapsed time: {total_elapsed_time_str}")


if __name__ == "__main__":
    main()
