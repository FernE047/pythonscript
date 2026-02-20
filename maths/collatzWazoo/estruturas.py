import shelve
from math import log


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
        formula_a: "Formula",
        output_proof: str,
    ) -> "tuple[str, ModulusRule | None]":
        text = "x=y?\n"
        factor_a = formula_a.a
        ofsset_a = formula_a.b
        divisor_a = formula_a.c
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
            e7 = factor_d
            is_satisfied = False
            for d7 in range(e7):
                factor_f = e7 * factor_e
                offset_f = factor_e * d7 + offset_e
                if (factor_f % factor_d == 0) and (offset_f % factor_d == 0):
                    text += f"{factor_d}k={factor_e}({e7}m+{d7})+{offset_e}\n"
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
        e10 = self.divisor * factor_final
        d10 = self.divisor * offset_final + self.remainder
        text += f"x={e10}n+{d10}\n\n"
        output_proof += text
        return (output_proof, ModulusRule(e10, d10))

    def set_remainder(self, new_remainder: int) -> None:
        self.remainder = self.testaResto(new_remainder)

#TODO: stopped coding here

    def testaResto(self, new_remainder: int) -> int:
        return int(new_remainder) % self.divisor

    def copia(self) -> "ModulusRule":
        return ModulusRule(self.divisor, self.remainder)

    def puro(self) -> list[int]:
        return [self.divisor, self.remainder]

    def __str__(self) -> str:
        return self.create_simple_text(self.display_value)


class Formula:
    a: int
    b: int
    c: int

    def __init__(
        self, a: list[int] | int = 1, b: list[int] | int = 0, c: list[int] | int = 1
    ) -> None:
        if isinstance(a, list):
            self.a = a[0]
        else:
            self.a = a
        if isinstance(b, list):
            self.b = b[0]
        else:
            self.b = b
        if isinstance(c, list):
            self.c = c[0]
        else:
            self.c = c
        self.varApresentacao = "x"

    def numeroTeste(self, numero: int) -> bool:
        return ((self.a * numero + self.b) % self.c) == 0

    def numeroValor(self, numero: int) -> int | None:
        if self.numeroTeste(numero):
            return (self.a * numero + self.b) // self.c
        else:
            return None

    def valor(self, x: int) -> float:
        return (self.a * x + self.b) / self.c

    def setVarApresentacao(self, letra: str) -> None:
        self.varApresentacao = str(letra)

    def textSimples(self, x: str) -> str:
        text = str(x)
        if self.b != 0:
            if self.b > 0:
                text += f"+{self.b}"
            else:
                text += f"{self.b}"
            if self.c != 1:
                text += f")/{self.c}"
                if self.a != 1:
                    return f"({self.a}{text}"
                else:
                    return f"({text}"
            else:
                if self.a != 1:
                    return f"{self.a}{text}"
                else:
                    return text
        else:
            if self.c != 1:
                text += f"/{self.c}"
            if self.a != 1:
                text = f"{self.a}{text}"
            return text

    def inversa(self) -> "Formula":
        return Formula(self.c, -self.b, self.a)

    def aplica(self, outraFormula: "Formula") -> "Formula":
        newA = self.a * outraFormula.a
        newC = self.c * outraFormula.c
        newB = self.a * outraFormula.b + self.b * outraFormula.c
        return Formula(newA, newB, newC)

    def outFormato(self, inFormato: "ModulusRule") -> "ModulusRule":
        saidaFormato = inFormato.copia()
        saidaFormato.set_divisor((inFormato.divisor * self.a) // self.c)
        saidaFormato.set_remainder((inFormato.remainder * self.a + self.b) // self.c)
        return saidaFormato

    def simplifica(self) -> None:
        j = get_greatest_2_and_3_factors([self.a, self.b, self.c])
        self.a = self.a // j
        self.b = self.b // j
        self.c = self.c // j

    def copia(self) -> "Formula":
        return Formula(self.a, self.b, self.c)

    def pura(self) -> list[int]:
        return [self.a, self.b, self.c]

    def __str__(self) -> str:
        return self.textSimples(self.varApresentacao)


class Regra:
    def __init__(
        self,
        formato: ModulusRule | list[int] | None = None,
        formula: Formula | None = None,
        tipo: str = "ativa",
    ) -> None:
        if formato is None:
            raise TypeError("formato must be provided")
        if isinstance(formato, list):
            self.setFormato(formato[:2])
            self.setFormula(formato[2:])
        else:
            self.setFormato(formato)
            self.setFormula(formula)
        self.tipo = tipo

    def setFormula(self, formula: Formula | list[int] | None) -> None:
        if formula is None:
            self.formula = Formula()
        elif isinstance(formula, list):
            self.formula = Formula(formula)
        else:
            self.formula = formula

    def setFormato(self, formato: ModulusRule | list[int] | None) -> None:
        if formato:
            if isinstance(formato, list):
                self.formato = ModulusRule(formato)
            else:
                self.formato = formato
        else:
            self.formato = ModulusRule(1)

    def setTipo(self, novoTipo: str) -> None:
        self.tipo = novoTipo

    def getFormula(self) -> Formula:
        return self.formula.copia()

    def getFormato(self) -> ModulusRule:
        a = self.formato
        return a.copia()

    def getTipo(self) -> str:
        return self.tipo

    def aplicaRegra(self, numero: int) -> float:
        return self.getFormula().valor(numero)

    def testaRegra(self, numero: int) -> bool:
        return self.getFormato().test_number(numero)

    def inversa(self) -> "Regra":
        formulaRegra = self.getFormula()
        formatoRegra = self.getFormato()
        formatoInverso = formulaRegra.outFormato(formatoRegra)
        formulaInversa = formulaRegra.inversa()
        return Regra(formatoInverso, formulaInversa, self.tipo)

    def copia(self) -> "Regra":
        return Regra(self.getFormato(), self.getFormula(), self.getTipo())

    def solve(
        self, regra: "Regra", output_proof: str
    ) -> tuple[str, ModulusRule | None]:
        formulaArg = self.getFormula()
        formatoArg = regra.getFormato()
        return self.getFormato().solve(
            formatoArg, formulaArg, output_proof=output_proof
        )

    def pura(self) -> list[int]:
        return self.getFormato().puro() + self.getFormula().pura()

    def __str__(self) -> str:
        return f"{str(self.getFormato()):20} : {str(self.getFormula()):20}"


class Collatz_Function:
    def __init__(self, listaRegras: list[Regra] | None = None) -> None:
        self.regras: list[Regra] = []
        self.regraQuant = 0
        if listaRegras:
            for regra in listaRegras:
                self.addRegra(regra)

    def addRegra(
        self, regra: Regra | list[int] | None, tipo: str | None = None
    ) -> None:
        if regra is None:
            return
        if isinstance(regra, list):
            if len(regra) == 0:
                return
            if tipo is None:
                tipo = "normal"
            self.regras.append(Regra(regra, tipo=tipo))
        else:
            if tipo is not None:
                regra.setTipo(tipo)
            self.regras.append(regra)
        self.regraQuant += 1

    def popRegra(self, index: int) -> None:
        if index < self.regraQuant:
            self.regras.pop(index)
            self.regraQuant -= 1

    def getRegra(self, index: int) -> Regra | None:
        if index > self.regraQuant:
            return None
        return self.regras[index]

    def get_rules(self, tiposDados: list[str] | None = None) -> list[Regra]:
        tiposDados = tiposDados if tiposDados else []
        lista: list[Regra] = []
        for regra in self.regras:
            if tiposDados:
                if regra.getTipo() in tiposDados:
                    lista.append(regra.copia())
            else:
                lista.append(regra.copia())
        return lista

    def getTipos(self) -> list[str]:
        all_tipos: set[str] = set()
        for regra in self.regras:
            tipo = regra.getTipo()
            all_tipos.add(tipo)
        return list(all_tipos)

    def aplicaFuncao(self, x: int) -> list[int]:
        lista: list[int] = []
        for regra in self.regras:
            if regra.testaRegra(x):
                lista.append(int(regra.aplicaRegra(x)))
        return lista

    def regrasAplicadasA(self, x: int) -> list[int]:
        lista: list[int] = []
        for index, regra in enumerate(self.regras):
            if regra.testaRegra(x):
                lista.append(index)
        return lista

    def formatosRestantes(self) -> None:
        pass  # TODO: implement this

    def copia(self) -> "Collatz_Function":
        lista: list[Regra] = []
        for regra in self.regras:
            lista.append(regra.copia())
        return Collatz_Function(lista)

    def inversa(self) -> "Collatz_Function":
        lista: list[Regra] = []
        for regra in self.regras:
            lista.append(regra.inversa())
        return Collatz_Function(lista)

    def passos(self, x: int) -> list[int]:
        lista: list[int] = []
        while x not in lista:
            aplicacao = self.aplicaFuncao(x)
            if aplicacao:
                lista.append(x)
                x = aplicacao[0]
            else:
                lista = []
                return lista
        lista.append(x)
        return lista

    def passosLoop(self, x: int) -> int:
        return len(self.passos(x)) - 1

    def valoresEmPassos(self, passos: int) -> list[int]:
        funcaoInversa = self.inversa()
        novaLista = [1]
        for _ in range(passos - 1):
            lista = novaLista
            novaLista = []
            for elemento in lista:
                novaLista += funcaoInversa.aplicaFuncao(elemento)
        return sorted(novaLista)

    def valoresEmPassosComLimites(
        self, passos: int, limite: int, inicio: int = 1
    ) -> list[int]:
        lista: list[int] = []
        for a in range(inicio, limite + 1):
            if self.passosLoop(a) <= passos:
                lista.append(a)
        return lista

    def estruturaReal(self) -> "Collatz_Function":
        funcaoReal = Collatz_Function(self.get_rules(["principal", "ativa"]))
        return funcaoReal

    def estruturaUtil(self) -> "Collatz_Function":
        funcaoUtil = Collatz_Function(self.get_rules(["passiva"]))
        return funcaoUtil

    def estruturaUtilFutura(self) -> "Collatz_Function":
        funcaoUtil = Collatz_Function(self.get_rules(["principal", "passiva"]))
        return funcaoUtil

    def salva(self, indice: int) -> None:
        with shelve.open("collatzRegras") as BD:
            lista: list[tuple[list[int], str]] = []
            for tipo in self.getTipos():
                for regra in self.get_rules([tipo]):
                    lista.append((regra.pura(), tipo))
            BD[f"collatz{indice}"] = lista

    def apresentacao(self) -> str:
        text = ""
        index = 0
        for tipo in self.getTipos():
            text += f"\n{tipo}\n\n"
            for regra in self.get_rules([tipo]):
                text += f"{index:03d} : "
                formato = regra.getFormato()
                text += f"2^{int(log(formato.divisor, 2)):02d}k+{formato.remainder}"
                text += f"{index} : {str(regra)}\n"
                index += 1
        return text

    def __str__(self):
        text = ""
        index = 0
        for tipo in self.getTipos():
            text += f"\n{tipo}\n\n"
            for regra in self.get_rules([tipo]):
                text += f"{index:02d} : {str(regra)}\n"
                index += 1
        return text


def Collatz(indice: int) -> Collatz_Function:
    with shelve.open("collatzRegras") as BD:
        collatz = Collatz_Function()
        for regraSimples in BD[f"collatz{indice}"]:
            argumento = regraSimples[0]
            tipoArg = regraSimples[1]
            collatz.addRegra(argumento, tipo=tipoArg)
    return collatz.copia()


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
    for a in range(7):
        print(f"\n\ncollatz {a}\n\n")
        print(Collatz(a))


if __name__ == "__main__":
    main()
