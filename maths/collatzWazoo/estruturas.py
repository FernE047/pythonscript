from io import TextIOWrapper
import shelve
from math import log


class Formato:
    def __init__(self, divisor: list[int] | int, resto: int = 0) -> None:
        if isinstance(divisor, list):
            self.setDivisor(divisor[0])
            self.setResto(divisor[1])
        else:
            self.setDivisor(divisor)
            self.setResto(resto)
        self.varApresentacao = "k"

    def numeroTeste(self, numero: int) -> bool:
        return (numero % self.divisor) == self.resto

    def numeroValor(self, numero: int) -> int | None:
        if self.numeroTeste(numero):
            return (numero - self.resto) // self.divisor
        else:
            return None

    def valor(self, k: int) -> int:
        return self.divisor * k + self.resto

    def aplica(self, outroFormato: "Formato") -> "Formato":
        newDivisor = self.divisor * outroFormato.divisor
        newResto = self.divisor * outroFormato.resto + self.resto
        return Formato(newDivisor, newResto)

    def aplicado(self, outroFormato: "Formato") -> "Formato":
        return outroFormato.aplica(self)

    def setVarApresentacao(self, letra: str) -> None:
        self.varApresentacao = str(letra)

    def textoSimples(self, k: str) -> str:
        texto = "{}*{}".format(self.divisor, k)
        if self.resto:
            texto += "+{}".format(self.resto)
        return texto

    def textoComposto(self, k: int) -> str:
        texto = "{}".format(self.divisor * k)
        if self.resto:
            texto += "+{}".format(self.resto)
        return texto

    def setDivisor(self, novoDivisor: int) -> None:
        if novoDivisor == 0:
            self.divisor = 1
        else:
            self.divisor = int(novoDivisor)

    def resolvePara(
        self,
        formato2: "Formato",
        formula: "Formula",
        saida: str | TextIOWrapper = "padrao",
    ) -> "Formato | None":
        texto = "x=y?\n"
        a = formula.a
        b = formula.b
        c = formula.c
        texto += "({}x+{})/{}=y\n".format(a, b, c)
        e0 = self.divisor
        d0 = self.resto
        e1 = formato2.divisor
        d1 = formato2.resto
        texto += "{}({}k+{})+{}={}({}n+{})\n".format(a, e0, d0, b, c, e1, d1)
        e2 = a * e0
        d2 = a * d0 + b
        e3 = c * e1
        d3 = c * d1
        texto += "{}k+{}={}n+{}\n".format(e2, d2, e3, d3)
        d4 = (d3 - d2) % e3
        texto += "{}k={}n+{}\n".format(e2, e3, d4)
        j = mdc([e2, e3, d4])
        texto += "j = mdc({},{},{}) = {}\n".format(e2, e3, d4, j)
        e6 = e2 // j
        e5 = e3 // j
        d5 = d4 // j
        e8 = 1
        d8 = 1
        e9 = 1
        d9 = 1
        texto += "{}k={}n+{}\n".format(e6, e5, d5)
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
                    texto += "{}k={}({}m+{})+{}\n".format(e6, e5, e7, d7, d5)
                    right = True
                    break
            if not (right):
                texto += "contradiz\n\n"
                if saida == "padrao":
                    print(texto)
                else:
                    saida.write(texto)  # type: ignore
                return None
        if e6 != 1:
            texto += "{}k={}n+{}\n".format(e6, e8, d8)
            if (e8 % e6 == 0) and (d8 % e6 == 0):
                e9 = e8 // e6
                d9 = d8 // e6
                e6 = 1
                texto += "{}k={}n+{}\n".format(e6, e9, d9)
        else:
            e9 = e8
            d9 = d8
        texto += "x={}({}n+{})+{}\n".format(e0, e9, d9, d0)
        e10 = e0 * e9
        d10 = e0 * d9 + d0
        texto += "x={}n+{}\n\n".format(e10, d10)
        if saida == "padrao":
            print(texto)
        else:
            saida.write(texto)  # type: ignore
        return Formato(e10, d10)

    def setResto(self, novoResto: int) -> None:
        self.resto = self.testaResto(novoResto)

    def testaResto(self, novoResto: int) -> int:
        return int(novoResto) % self.divisor

    def copia(self) -> "Formato":
        return Formato(self.divisor, self.resto)

    def puro(self) -> list[int]:
        return [self.divisor, self.resto]

    def __str__(self) -> str:
        return self.textoSimples(self.varApresentacao)


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
                texto += "+" + str(self.b)
            else:
                texto += str(self.b)
            if self.c != 1:
                texto += ")/" + str(self.c)
                if self.a != 1:
                    return "(" + str(self.a) + texto
                else:
                    return "(" + texto
            else:
                if self.a != 1:
                    return str(self.a) + texto
                else:
                    return texto
        else:
            if self.c != 1:
                texto += "/" + str(self.c)
            if self.a != 1:
                texto = str(self.a) + texto
            return texto

    def inversa(self) -> "Formula":
        return Formula(self.c, -self.b, self.a)

    def aplica(self, outraFormula: "Formula") -> "Formula":
        newA = self.a * outraFormula.a
        newC = self.c * outraFormula.c
        newB = self.a * outraFormula.b + self.b * outraFormula.c
        return Formula(newA, newB, newC)

    def outFormato(self, inFormato: "Formato") -> "Formato":
        saidaFormato = inFormato.copia()
        saidaFormato.setDivisor((inFormato.divisor * self.a) // self.c)
        saidaFormato.setResto((inFormato.resto * self.a + self.b) // self.c)
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
        formato: Formato | list[int] | None = None,
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

    def setFormato(self, formato: Formato | list[int] | None) -> None:
        if formato:
            if isinstance(formato, list):
                self.formato = Formato(formato)
            else:
                self.formato = formato
        else:
            self.formato = Formato(1)

    def setTipo(self, novoTipo: str) -> None:
        self.tipo = novoTipo

    def getFormula(self) -> Formula:
        return self.formula.copia()

    def getFormato(self) -> Formato:
        a = self.formato
        return a.copia()

    def getTipo(self) -> str:
        return self.tipo

    def aplicaRegra(self, numero: int) -> float:
        return self.getFormula().valor(numero)

    def testaRegra(self, numero: int) -> bool:
        return self.getFormato().numeroTeste(numero)

    def inversa(self) -> "Regra":
        formulaRegra = self.getFormula()
        formatoRegra = self.getFormato()
        formatoInverso = formulaRegra.outFormato(formatoRegra)
        formulaInversa = formulaRegra.inversa()
        return Regra(formatoInverso, formulaInversa, self.tipo)

    def copia(self) -> "Regra":
        return Regra(self.getFormato(), self.getFormula(), self.getTipo())

    def resolvePara(
        self, regra: "Regra", saida: str | TextIOWrapper = "padrao"
    ) -> Formato | None:
        formulaArg = self.getFormula()
        formatoArg = regra.getFormato()
        return self.getFormato().resolvePara(formatoArg, formulaArg, saida=saida)

    def pura(self) -> list[int]:
        return self.getFormato().puro() + self.getFormula().pura()

    def __str__(self) -> str:
        return "{:20} : {:20}".format(str(self.getFormato()), str(self.getFormula()))


class Funcao:
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

    def getRegras(self, tiposDados: list[str] | None = None) -> list[Regra]:
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

    def copia(self) -> "Funcao":
        lista: list[Regra] = []
        for regra in self.regras:
            lista.append(regra.copia())
        return Funcao(lista)

    def inversa(self) -> "Funcao":
        lista: list[Regra] = []
        for regra in self.regras:
            lista.append(regra.inversa())
        return Funcao(lista)

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

    def valoresEmPassos(self, passos:int) -> list[int]:
        funcaoInversa = self.inversa()
        novaLista = [1]
        for _ in range(passos - 1):
            lista = novaLista
            novaLista = []
            for elemento in lista:
                novaLista += funcaoInversa.aplicaFuncao(elemento)
        return sorted(novaLista)

    def valoresEmPassosComLimites(self, passos: int, limite:int, inicio:int=1) -> list[int]:
        lista: list[int] = []
        for a in range(inicio, limite + 1):
            if self.passosLoop(a) <= passos:
                lista.append(a)
        return lista

    def estruturaReal(self) -> "Funcao":
        funcaoReal = Funcao(self.getRegras(["principal", "ativa"]))
        return funcaoReal

    def estruturaUtil(self) -> "Funcao":
        funcaoUtil = Funcao(self.getRegras(["passiva"]))
        return funcaoUtil

    def estruturaUtilFutura(self) -> "Funcao":
        funcaoUtil = Funcao(self.getRegras(["principal", "passiva"]))
        return funcaoUtil

    def salva(self, indice:int) -> None:
        BD = shelve.open("collatzRegras")
        lista:list[tuple[list[int],str]] = []
        for tipo in self.getTipos():
            for regra in self.getRegras([tipo]):
                lista.append((regra.pura(), tipo))
        BD["collatz{}".format(indice)] = lista
        BD.close()

    def apresentacao(self)-> str:
        texto = ""
        index = 0
        for tipo in self.getTipos():
            texto += "\n" + tipo + "\n\n"
            for regra in self.getRegras([tipo]):
                texto += "{:03d} : ".format(index)
                formato = regra.getFormato()
                texto += "2^{:02d}k+{}".format(
                    int(log(formato.divisor, 2)), formato.resto
                )
                texto += "{} : {}".format(index, str(regra)) + "\n"
                index += 1
        return texto

    def __str__(self):
        texto = ""
        index = 0
        for tipo in self.getTipos():
            texto += "\n" + tipo + "\n\n"
            for regra in self.getRegras([tipo]):
                texto += "{:02d} : {}".format(index, str(regra)) + "\n"
                index += 1
        return texto


def Collatz(indice:int) -> Funcao:
    BD = shelve.open("collatzRegras")
    collatz = Funcao()
    for regraSimples in BD["collatz{}".format(indice)]:
        argumento = regraSimples[0]
        tipoArg = regraSimples[1]
        collatz.addRegra(argumento, tipo=tipoArg)
    BD.close()
    return collatz.copia()


def mdcC(lista:list[int]) -> int:
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


def mdc(lista:list[int]) -> int:
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


if __name__ == "__main__":
    for a in range(7):
        print("\n\ncollatz {}\n\n".format(a))
        print(Collatz(a))
