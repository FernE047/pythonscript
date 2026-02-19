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

    def set_display_value(self, letra: str) -> None:
        self.display_value = str(letra)

#TODO: stopped here

    def textoSimples(self, k: str) -> str:
        texto = f"{self.divisor}*{k}"
        if self.remainder:
            texto += f"+{self.remainder}"
        return texto

    def textoComposto(self, k: int) -> str:
        texto = f"{self.divisor * k}"
        if self.remainder:
            texto += f"+{self.remainder}"
        return texto

    def set_divisor(self, novoDivisor: int) -> None:
        if novoDivisor == 0:
            self.divisor = 1
        else:
            self.divisor = int(novoDivisor)

    def resolvePara(
        self,
        formato2: "ModulusRule",
        formula: "Formula",
        saida: str = "padrao",
    ) -> "ModulusRule | None":
        texto = "x=y?\n"
        a = formula.a
        b = formula.b
        c = formula.c
        texto += f"({a}x+{b})/{c}=y\n"
        e0 = self.divisor
        d0 = self.remainder
        e1 = formato2.divisor
        d1 = formato2.remainder
        texto += f"{a}({e0}k+{d0})+{b}={c}({e1}n+{d1})\n"
        e2 = a * e0
        d2 = a * d0 + b
        e3 = c * e1
        d3 = c * d1
        texto += f"{e2}k+{d2}={e3}n+{d3}\n"
        d4 = (d3 - d2) % e3
        texto += f"{e2}k={e3}n+{d4}\n"
        j = mdc([e2, e3, d4])
        texto += f"j = mdc({e2},{e3},{d4}) = {j}\n"
        e6 = e2 // j
        e5 = e3 // j
        d5 = d4 // j
        e8 = 1
        d8 = 1
        e9 = 1
        d9 = 1
        texto += f"{e6}k={e5}n+{d5}\n"
        if (e5 % e6 == 0) and (d5 % e6 == 0):
            e8 = e5 // e6
            d8 = d5 // e6
        else:
            e7 = e6
            right = False
            for d7 in range(e7):
                e8 = e7 * e5
                d8 = e5 * d7 + d5
                if (e8 % e6 == 0) and (d8 % e6 == 0):
                    texto += f"{e6}k={e5}({e7}m+{d7})+{d5}\n"
                    right = True
                    break
            if not (right):
                texto += "contradiz\n\n"
                saida += texto
                return None
        if e6 != 1:
            texto += f"{e6}k={e8}n+{d8}\n"
            if (e8 % e6 == 0) and (d8 % e6 == 0):
                e9 = e8 // e6
                d9 = d8 // e6
                e6 = 1
                texto += f"{e6}k={e9}n+{d9}\n"
        else:
            e9 = e8
            d9 = d8
        texto += f"x={e0}({e9}n+{d9})+{d0}\n"
        e10 = e0 * e9
        d10 = e0 * d9 + d0
        texto += f"x={e10}n+{d10}\n\n"
        saida += texto
        return ModulusRule(e10, d10)

    def set_remainder(self, novoResto: int) -> None:
        self.remainder = self.testaResto(novoResto)

    def testaResto(self, novoResto: int) -> int:
        return int(novoResto) % self.divisor

    def copia(self) -> "ModulusRule":
        return ModulusRule(self.divisor, self.remainder)

    def puro(self) -> list[int]:
        return [self.divisor, self.remainder]

    def __str__(self) -> str:
        return self.textoSimples(self.display_value)


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

    def textoSimples(self, x: str) -> str:
        texto = str(x)
        if self.b != 0:
            if self.b > 0:
                texto += f"+{self.b}"
            else:
                texto += f"{self.b}"
            if self.c != 1:
                texto += f")/{self.c}"
                if self.a != 1:
                    return f"({self.a}{texto}"
                else:
                    return f"({texto}"
            else:
                if self.a != 1:
                    return f"{self.a}{texto}"
                else:
                    return texto
        else:
            if self.c != 1:
                texto += f"/{self.c}"
            if self.a != 1:
                texto = f"{self.a}{texto}"
            return texto

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
        j = mdc([self.a, self.b, self.c])
        self.a = self.a // j
        self.b = self.b // j
        self.c = self.c // j

    def copia(self) -> "Formula":
        return Formula(self.a, self.b, self.c)

    def pura(self) -> list[int]:
        return [self.a, self.b, self.c]

    def __str__(self) -> str:
        return self.textoSimples(self.varApresentacao)


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

    def resolvePara(self, regra: "Regra", saida: str) -> ModulusRule | None:
        formulaArg = self.getFormula()
        formatoArg = regra.getFormato()
        return self.getFormato().resolvePara(formatoArg, formulaArg, saida=saida)

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
        texto = ""
        index = 0
        for tipo in self.getTipos():
            texto += f"\n{tipo}\n\n"
            for regra in self.get_rules([tipo]):
                texto += f"{index:03d} : "
                formato = regra.getFormato()
                texto += f"2^{int(log(formato.divisor, 2)):02d}k+{formato.remainder}"
                texto += f"{index} : {str(regra)}\n"
                index += 1
        return texto

    def __str__(self):
        texto = ""
        index = 0
        for tipo in self.getTipos():
            texto += f"\n{tipo}\n\n"
            for regra in self.get_rules([tipo]):
                texto += f"{index:02d} : {str(regra)}\n"
                index += 1
        return texto


def Collatz(indice: int) -> Collatz_Function:
    with shelve.open("collatzRegras") as BD:
        collatz = Collatz_Function()
        for regraSimples in BD[f"collatz{indice}"]:
            argumento = regraSimples[0]
            tipoArg = regraSimples[1]
            collatz.addRegra(argumento, tipo=tipoArg)
    return collatz.copia()


def mdcC(lista: list[int]) -> int:
    novaLista: list[int] = []
    for elemento in lista:
        if elemento < 0:
            novaLista.append(-elemento)
        elif elemento > 0:
            novaLista.append(elemento)
    for d in range(min(novaLista), 0, -1):
        cont = False
        for elemento in novaLista:
            if elemento % d != 0:
                cont = True
        if not (cont):
            return d
    return 1


def mdc(lista: list[int]) -> int:
    novaLista: list[int] = []
    for elemento in lista:
        if elemento < 0:
            novaLista.append(-elemento)
        elif elemento > 0:
            novaLista.append(elemento)
    n2 = 0
    n3 = 0
    while True:
        cont = False
        for elemento in novaLista:
            if elemento % (2**n2) != 0:
                cont = True
        if not (cont):
            n2 += 1
        else:
            n2 -= 1
            break
    while True:
        cont = False
        for elemento in novaLista:
            if elemento % (3**n3) != 0:
                cont = True
        if not (cont):
            n3 += 1
        else:
            n3 -= 1
            break
    return (2**n2) * (3**n3)


def main() -> None:
    for a in range(7):
        print(f"\n\ncollatz {a}\n\n")
        print(Collatz(a))


if __name__ == "__main__":
    main()
