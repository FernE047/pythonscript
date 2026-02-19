from estruturas import Collatz
from estruturas import Collatz_Function
from estruturas import Regra
from time import time


def print_elapsed_time(seconds: float) -> None:
    if seconds < 0:
        seconds = -seconds
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(seconds * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    print(f"{sign}{', '.join(parts)}")


def main() -> None:
    from_collatz = 5  # min=2
    to_collatz = 6
    next_collatz = Collatz(from_collatz)
    execution_times: list[float] = []
    for collatz_level in range(from_collatz, to_collatz):
        start_time = time()
        current_collatz = next_collatz
        next_collatz = Collatz_Function()
        text_proof = f"{current_collatz}\n"
        core_rules = current_collatz.get_rules(["principal"])
        generative_rules = current_collatz.get_rules(["ativa"])
        passive_rules = current_collatz.get_rules(["passiva"])
        for rule in passive_rules:
            next_collatz.addRegra(rule.copia())
        for rule in core_rules:
            new_rule = rule.copia()
            new_rule.setTipo("passiva")
            next_collatz.addRegra(new_rule)
        for rule_1 in generative_rules:
            for rule_2 in current_collatz.estruturaReal().get_rules():
                text_proof += "passo 1 :\n\n\n"
                new_formato = rule_1.resolvePara(rule_2, text_proof)
                text_proof += "\n"
                if new_formato is None:
                    continue
                new_formula = rule_1.getFormula().copia()
                if rule_2.getTipo() == "ativa":
                    new_rule = Regra(new_formato, new_formula, "ativa")
                    next_collatz.addRegra(new_rule)
                    continue
                for rule_3 in generative_rules:
                    text_proof = f"\n{rule_1}\n{rule_2}\n{rule_3}\n"
                    formula_1 = rule_1.getFormula().copia()
                    formula_2 = rule_2.getFormula().copia()
                    formula_3 = rule_3.getFormula().inversa().copia()
                    text_proof += f"{formula_1}\n{formula_2}\n{formula_3}\n"
                    formula_4 = formula_3.aplica(formula_2.aplica(formula_1))
                    text_proof += f"{formula_4}\n"
                    target_format = rule_3.getFormato()
                    text_proof += f"{formula_4}\n{new_formato}\n{target_format}\n"
                    new_formato_2 = new_formato.resolvePara(
                        target_format, formula_4, text_proof
                    )
                    text_proof += f"teste : {new_formato_2}\n"
                    if new_formato_2 is None:
                        continue
                    new_rule = Regra(new_formato_2, formula_4, "principal")
                    next_collatz.addRegra(new_rule)
        filename = f"collatz{collatz_level}de{collatz_level + 1}.txt"
        with open(filename, "w", encoding="utf-8") as proof_file:
            proof_file.write(text_proof)
        end_time = time()
        print(f"collatz {collatz_level + 1} : ")
        print(next_collatz)
        next_collatz.salva(collatz_level + 1)
        execution_times.append(end_time - start_time)
        print_elapsed_time(execution_times[-1])
        print("\n")
    if len(execution_times) > 1:
        print("total : ")
        print_elapsed_time(sum(execution_times))


if __name__ == "__main__":
    main()
