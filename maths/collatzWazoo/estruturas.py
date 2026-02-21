import shelve
from math import log
from typing import Literal

EquationTypeOptions = Literal["core", "generative", "passive"]


class ModulusRule:
    def __init__(self, divisor: list[int] | int, remainder: int = 0) -> None:
        if isinstance(divisor, list):
            self.set_divisor(divisor[0])
            self.set_remainder(divisor[1])
        else:
            self.set_divisor(divisor)
            self.set_remainder(remainder)
        self.display_value = "k"

    def test_number(self, value_to_test: int) -> bool:
        return (value_to_test % self.divisor) == self.remainder

    def calculate_value(self, value_to_test: int) -> int | None:
        if self.test_number(value_to_test):
            return (value_to_test - self.remainder) // self.divisor
        return None

    def compute_result(self, k: int) -> int:
        return self.divisor * k + self.remainder

    def apply_modulus_rule(self, other: "ModulusRule") -> "ModulusRule":
        new_divisor = self.divisor * other.divisor
        new_remainder = self.divisor * other.remainder + self.remainder
        return ModulusRule(new_divisor, new_remainder)

    def apply_modulus_to_self(self, other: "ModulusRule") -> "ModulusRule":
        return other.apply_modulus_rule(self)

    def set_display_value(self, display_character: str) -> None:
        self.display_value = str(display_character)

    def create_simple_text(self, display_character: str) -> str:
        formatted_expression = f"{self.divisor}*{display_character}"
        if self.remainder:
            formatted_expression += f"+{self.remainder}"
        return formatted_expression

    def create_composite_text(self, factor: int) -> str:
        formatted_expression = f"{self.divisor * factor}"
        if self.remainder:
            formatted_expression += f"+{self.remainder}"
        return formatted_expression

    def set_divisor(self, new_divisor: int) -> None:
        if new_divisor == 0:
            self.divisor = 1
        else:
            self.divisor = int(new_divisor)

    def solve(
        self,
        modulus_rule_a: "ModulusRule",
        formula_a: "MathExpression",
        output_proof: str,
    ) -> "tuple[str, ModulusRule | None]":
        text = "x=y?\n"
        factor_a = formula_a.factor
        ofsset_a = formula_a.offset
        divisor_a = formula_a.divisor
        text += f"({factor_a}x+{ofsset_a})/{divisor_a}=y\n"
        modulus_divisor_a = modulus_rule_a.divisor
        modulus_remainder_a = modulus_rule_a.remainder
        text += f"{factor_a}({self.divisor}k+{self.remainder})+{ofsset_a}={divisor_a}({modulus_divisor_a}n+{modulus_remainder_a})\n"
        factor_b = factor_a * self.divisor
        offset_b = factor_a * self.remainder + ofsset_a
        factor_c = divisor_a * modulus_divisor_a
        offset_c = divisor_a * modulus_remainder_a
        text += f"{factor_b}k+{offset_b}={factor_c}n+{offset_c}\n"
        derived_offset = (offset_c - offset_b) % factor_c
        text += f"{factor_b}k={factor_c}n+{derived_offset}\n"
        greatest_common_divisor = get_greatest_2_and_3_factors(
            [factor_b, factor_c, derived_offset]
        )
        text += f"j = mdc({factor_b},{factor_c},{derived_offset}) = {greatest_common_divisor}\n"
        factor_d = factor_b // greatest_common_divisor
        factor_e = factor_c // greatest_common_divisor
        offset_e = derived_offset // greatest_common_divisor
        factor_f = 1
        offset_f = 1
        factor_final = 1
        offset_final = 1
        text += f"{factor_d}k={factor_e}n+{offset_e}\n"
        if (factor_e % factor_d == 0) and (offset_e % factor_d == 0):
            factor_f = factor_e // factor_d
            offset_f = offset_e // factor_d
        else:
            factor_helper = factor_d
            is_satisfied = False
            for offset_helper in range(factor_helper):
                factor_f = factor_helper * factor_e
                offset_f = factor_e * offset_helper + offset_e
                if (factor_f % factor_d == 0) and (offset_f % factor_d == 0):
                    text += f"{factor_d}k={factor_e}({factor_helper}m+{offset_helper})+{offset_e}\n"
                    is_satisfied = True
                    break
            if not (is_satisfied):
                text += "contradiz\n\n"
                output_proof += text
                return (output_proof, None)
        if factor_d != 1:
            text += f"{factor_d}k={factor_f}n+{offset_f}\n"
            if (factor_f % factor_d == 0) and (offset_f % factor_d == 0):
                factor_final = factor_f // factor_d
                offset_final = offset_f // factor_d
                factor_d = 1
                text += f"{factor_d}k={factor_final}n+{offset_final}\n"
        else:
            factor_final = factor_f
            offset_final = offset_f
        text += f"x={self.divisor}({factor_final}n+{offset_final})+{self.remainder}\n"
        factor_rule = self.divisor * factor_final
        offset_rule = self.divisor * offset_final + self.remainder
        text += f"x={factor_rule}n+{offset_rule}\n\n"
        output_proof += text
        return (output_proof, ModulusRule(factor_rule, offset_rule))

    def set_remainder(self, new_remainder: int) -> None:
        self.remainder = self.calculate_remainder(new_remainder)

    def calculate_remainder(self, new_remainder: int) -> int:
        return int(new_remainder) % self.divisor

    def copy(self) -> "ModulusRule":
        return ModulusRule(self.divisor, self.remainder)

    def to_raw(self) -> list[int]:
        return [self.divisor, self.remainder]

    def __str__(self) -> str:
        return self.create_simple_text(self.display_value)


class MathExpression:
    factor: int
    offset: int
    divisor: int

    def __init__(
        self,
        factor: list[int] | int = 1,
        offset: list[int] | int = 0,
        divisor: list[int] | int = 1,
    ) -> None:
        if isinstance(factor, list):
            self.factor = factor[0]
        else:
            self.factor = factor
        if isinstance(offset, list):
            self.offset = offset[0]
        else:
            self.offset = offset
        if isinstance(divisor, list):
            self.divisor = divisor[0]
        else:
            self.divisor = divisor
        self.display_variable = "x"

    def check_divisibility(self, number: int) -> bool:
        return ((self.factor * number + self.offset) % self.divisor) == 0

    def calculate_value(self, number: int) -> int | None:
        if self.check_divisibility(number):
            return (self.factor * number + self.offset) // self.divisor
        else:
            return None

    def evaluate_expression(self, number: int) -> float:
        return (self.factor * number + self.offset) / self.divisor

    def set_display_var(self, display_char: str) -> None:
        self.display_variable = display_char

    def inverse_expression(self) -> "MathExpression":
        return MathExpression(self.divisor, -self.offset, self.factor)

    def combine_expressions(self, other: "MathExpression") -> "MathExpression":
        new_factor = self.factor * other.factor
        new_divisor = self.divisor * other.divisor
        new_offset = self.factor * other.offset + self.offset * other.divisor
        return MathExpression(new_factor, new_offset, new_divisor)

    def combine_with_modulus_rule(
        self, modulus_rule_input: "ModulusRule"
    ) -> "ModulusRule":
        new_rule = modulus_rule_input.copy()
        new_rule.set_divisor((modulus_rule_input.divisor * self.factor) // self.divisor)
        new_rule.set_remainder(
            (modulus_rule_input.remainder * self.factor + self.offset) // self.divisor
        )
        return new_rule

    def simplify(self) -> None:
        reduction_factor = get_greatest_2_and_3_factors(
            [self.factor, self.offset, self.divisor]
        )
        self.factor = self.factor // reduction_factor
        self.offset = self.offset // reduction_factor
        self.divisor = self.divisor // reduction_factor

    def copy(self) -> "MathExpression":
        return MathExpression(self.factor, self.offset, self.divisor)

    def to_raw(self) -> list[int]:
        return [self.factor, self.offset, self.divisor]

    def __str__(self) -> str:
        text = self.display_variable
        if self.offset == 0:
            if self.divisor != 1:
                text += f"/{self.divisor}"
            if self.factor != 1:
                text = f"{self.factor}{text}"
            return text
        if self.offset > 0:
            text += f"+{self.offset}"
        else:
            text += f"{self.offset}"
        if self.divisor != 1:
            text += f")/{self.divisor}"
            if self.factor != 1:
                return f"({self.factor}{text}"
            else:
                return f"({text}"
        if self.factor != 1:
            return f"{self.factor}{text}"
        else:
            return text


class Rule:
    equation_type: EquationTypeOptions

    def __init__(
        self,
        modulus_rule: ModulusRule | list[int] | None = None,
        equation: MathExpression | None = None,
        equation_type: EquationTypeOptions = "generative",
    ) -> None:
        if modulus_rule is None:
            raise TypeError("modulus_rule must be provided")
        if isinstance(modulus_rule, list):
            self.set_modulus_rule(modulus_rule[:2])
            self.set_equation(modulus_rule[2:])
        else:
            self.set_modulus_rule(modulus_rule)
            self.set_equation(equation)
        self.equation_type = equation_type

    def set_equation(self, equation: MathExpression | list[int] | None) -> None:
        if equation is None:
            self.equation = MathExpression()
        elif isinstance(equation, list):
            self.equation = MathExpression(equation)
        else:
            self.equation = equation

    def set_modulus_rule(self, modulus_input: ModulusRule | list[int] | None) -> None:
        if modulus_input is None:
            self.modulus_rule = ModulusRule(1)
            return
        if isinstance(modulus_input, list):
            self.modulus_rule = ModulusRule(modulus_input)
        else:
            self.modulus_rule = modulus_input

    def set_equation_type(self, new_type: EquationTypeOptions) -> None:
        self.equation_type = new_type

    def get_equation(self) -> MathExpression:
        return self.equation.copy()

    def get_modulus_rule(self) -> ModulusRule:
        return self.modulus_rule.copy()

    def get_equation_type(self) -> EquationTypeOptions:
        return self.equation_type

    def apply_rule(self, number: int) -> float:
        return self.get_equation().evaluate_expression(number)

    def test_rule(self, number: int) -> bool:
        return self.get_modulus_rule().test_number(number)

    def get_opposite_rule(self) -> "Rule":
        equation_copy = self.get_equation()
        modulus_rule_copy = self.get_modulus_rule()
        inverse_modulus_rule = equation_copy.combine_with_modulus_rule(
            modulus_rule_copy
        )
        inverse_equation = equation_copy.inverse_expression()
        return Rule(inverse_modulus_rule, inverse_equation, self.equation_type)

    def copy(self) -> "Rule":
        return Rule(
            self.get_modulus_rule(), self.get_equation(), self.get_equation_type()
        )

    def solve(self, regra: "Rule", output_proof: str) -> tuple[str, ModulusRule | None]:
        equation_copy = self.get_equation()
        modulus_rule_copy = regra.get_modulus_rule()
        return self.get_modulus_rule().solve(
            modulus_rule_copy, equation_copy, output_proof=output_proof
        )

    def to_raw(self) -> list[int]:
        return self.get_modulus_rule().to_raw() + self.get_equation().to_raw()

    def __str__(self) -> str:
        return f"{str(self.get_modulus_rule()):20} : {str(self.get_equation()):20}"


class Collatz_Function:
    def __init__(self, rule_list: list[Rule] | None = None) -> None:
        self.rule: list[Rule] = []
        self.rule_count = 0
        if rule_list:
            for rule in rule_list:
                self.append_rule(rule)

    def append_rule(
        self,
        rule: Rule | list[int] | None,
        equation_type: EquationTypeOptions | None = None,
    ) -> None:
        if rule is None:
            return
        if not isinstance(rule, list):
            if equation_type is not None:
                rule.set_equation_type(equation_type)
            self.rule.append(rule)
            self.rule_count += 1
            return
        if len(rule) == 0:
            return
        if equation_type is None:
            equation_type = "generative"
        self.rule.append(Rule(rule, equation_type=equation_type))
        self.rule_count += 1

    def pop_rule(self, index: int) -> None:
        if index < self.rule_count:
            self.rule.pop(index)
            self.rule_count -= 1

    def get_rule(self, index: int) -> Rule | None:
        if index >= self.rule_count:
            return None
        return self.rule[index]

    def get_rules(
        self, selected_equation_types: list[EquationTypeOptions] | None = None
    ) -> list[Rule]:
        if selected_equation_types is None:
            selected_equation_types = []
        rules_list: list[Rule] = []
        for rule in self.rule:
            if len(selected_equation_types) == 0:
                rules_list.append(rule.copy())
                continue
            if rule.get_equation_type() in selected_equation_types:
                rules_list.append(rule.copy())
        return rules_list

    def get_equation_type(self) -> list[EquationTypeOptions]:
        unique_equation_types: set[EquationTypeOptions] = set()
        for rule in self.rule:
            tipo = rule.get_equation_type()
            unique_equation_types.add(tipo)
        return list(unique_equation_types)

    def apply(self, number: int) -> list[int]:
        valid_results: list[int] = []
        for rule in self.rule:
            if rule.test_rule(number):
                valid_results.append(int(rule.apply_rule(number)))
        return valid_results

    def get_applied_rules(self, number: int) -> list[int]:
        applied_rule_indexes: list[int] = []
        for index, rule in enumerate(self.rule):
            if rule.test_rule(number):
                applied_rule_indexes.append(index)
        return applied_rule_indexes

    def available_modulus_rules(self) -> None:
        # TODO: implement this
        # we just gotta start at 2^1 and test if the modulus values are present in the rules.
        # the ones that are not present are added only if they are not incompleted by 2^n rules.
        pass

    def copy(self) -> "Collatz_Function":
        rules_copy: list[Rule] = []
        for rule in self.rule:
            rules_copy.append(rule.copy())
        return Collatz_Function(rules_copy)

    def get_opposite(self) -> "Collatz_Function":
        opposite_rules: list[Rule] = []
        for rule in self.rule:
            opposite_rules.append(rule.get_opposite_rule())
        return Collatz_Function(opposite_rules)

    def collatz_steps(self, number: int) -> list[int]:
        collatz_sequence: list[int] = []
        while number not in collatz_sequence:
            values = self.apply(number)
            if len(values) == 0:
                return []
            collatz_sequence.append(number)
            number = values[0]
        collatz_sequence.append(number)
        return collatz_sequence

    def get_steps_count(self, number: int) -> int:
        return len(self.collatz_steps(number)) - 1

    def generate_steps_values(self, step_count: int) -> list[int]:
        inverse_function = self.get_opposite()
        steps_value: list[int] = [1]
        for _ in range(step_count - 1):
            current_steps = steps_value
            steps_value = []
            for current_value in current_steps:
                steps_value.extend(inverse_function.apply(current_value))
        return sorted(steps_value)

    def generate_steps_values_limited(
        self, step_count: int, limit: int, start: int = 1
    ) -> list[int]:
        values: list[int] = []
        for number in range(start, limit + 1):
            if self.get_steps_count(number) <= step_count:
                values.append(number)
        return values

    def get_structural_function(self) -> "Collatz_Function":
        collatz_function = Collatz_Function(self.get_rules(["core", "generative"]))
        return collatz_function

    def get_util_function(self) -> "Collatz_Function":
        collatz_function = Collatz_Function(self.get_rules(["passive"]))
        return collatz_function

    def get_future_util_function(self) -> "Collatz_Function":
        collatz_function = Collatz_Function(self.get_rules(["core", "passive"]))
        return collatz_function

    def save_collatz_rules(self, index: int) -> None:
        collatz_rules_list: list[tuple[list[int], str]] = []
        for equation_type in self.get_equation_type():
            for rule in self.get_rules([equation_type]):
                collatz_rules_list.append((rule.to_raw(), equation_type))
        with shelve.open("collatzRegras") as database:
            database[f"collatz{index}"] = collatz_rules_list

    def dysplay(self) -> str:
        text = ""
        index = 0
        for equation_type in self.get_equation_type():
            text += f"\n{equation_type}\n\n"
            for rule in self.get_rules([equation_type]):
                text += f"{index:03d} : "
                formato = rule.get_modulus_rule()
                text += f"2^{int(log(formato.divisor, 2)):02d}k+{formato.remainder}"
                text += f"{index} : {str(rule)}\n"
                index += 1
        return text

    def __str__(self) -> str:
        text = ""
        index = 0
        for equation_type in self.get_equation_type():
            text += f"\n{equation_type}\n\n"
            for rule in self.get_rules([equation_type]):
                text += f"{index:02d} : {str(rule)}\n"
                index += 1
        return text


def load_collatz(index: int) -> Collatz_Function:
    with shelve.open("collatzRegras") as database:
        collatz = Collatz_Function()
        for simple_rule in database[f"collatz{index}"]:
            argument = simple_rule[0]
            equation_type = simple_rule[1]
            collatz.append_rule(argument, equation_type=equation_type)
    return collatz.copy()


def get_greatest_2_and_3_factors(input_values: list[int]) -> int:
    absolute_values: list[int] = []
    for elemento in input_values:
        if elemento < 0:
            absolute_values.append(-elemento)
        elif elemento > 0:
            absolute_values.append(elemento)
    two_factor_exponent = 0
    three_factor_exponent = 0
    while True:
        is_divisible = False
        for elemento in absolute_values:
            if elemento % (2**two_factor_exponent) != 0:
                is_divisible = True
        if is_divisible:
            two_factor_exponent -= 1
            break
        two_factor_exponent += 1
    while True:
        is_divisible = False
        for elemento in absolute_values:
            if elemento % (3**three_factor_exponent) != 0:
                is_divisible = True
        if is_divisible:
            three_factor_exponent -= 1
            break
        three_factor_exponent += 1
    return (2**two_factor_exponent) * (3**three_factor_exponent)


def main() -> None:
    for collatz_number in range(7):
        print(f"\n\ncollatz {collatz_number}\n\n")
        print(load_collatz(collatz_number))


if __name__ == "__main__":
    main()
