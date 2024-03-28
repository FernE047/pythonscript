import shelve
from math import log

class Formato:

    def __init__(self, divisor=1, resto=0):
        if(str(type(divisor))=="<class 'list'>"):
            self.setDivisor(divisor[0])
            self.setResto(divisor[1])
        else:
            self.setDivisor(divisor)
            self.setResto(resto)
        self.varApresentacao='k'

    def numeroTeste(self,numero):
        return((numero%self.divisor)==self.resto)

    def numeroValor(self,numero):
        if(self.numeroTeste(numero)):
            return (numero-self.resto)//self.divisor
        else:
            return None

    def valor(self,k):
        return self.divisor*k+self.resto

    def aplica(self,outroFormato):
        newDivisor=self.divisor*outroFormato.divisor
        newResto=self.divisor*outroFormato.resto+self.resto
        return Formato(newDivisor,newResto)

    def aplicado(self,outroFormato):
        return outroFormato.aplica(self)

    def setVarApresentacao(self,letra):
        self.varApresentacao=str(letra)

    def textoSimples(self,k):
        texto = '{}*{}'.format(self.divisor,k)
        if(self.resto):
            texto += '+{}'.format(self.resto)
        return texto

    def textoComposto(self,k):
        texto = '{}'.format(self.divisor*k)
        if(self.resto):
            texto += '+{}'.format(self.resto)
        return texto

    def setDivisor(self,novoDivisor):
        if(novoDivisor==0):
            self.divisor = 1
        else:
            self.divisor = int(novoDivisor)

    def resolvePara(self,formato2,formula,saida='padrao'):
        texto='x=y?\n'
        a=formula.a
        b=formula.b
        c=formula.c
        texto+='({}x+{})/{}=y\n'.format(a,b,c)
        e0=self.divisor
        d0=self.resto
        e1=formato2.divisor
        d1=formato2.resto
        texto+='{}({}k+{})+{}={}({}n+{})\n'.format(a,e0,d0,b,c,e1,d1)
        e2=a*e0
        d2=a*d0+b
        e3=c*e1
        d3=c*d1
        texto+='{}k+{}={}n+{}\n'.format(e2,d2,e3,d3)
        d4=(d3-d2)%e3
        texto+='{}k={}n+{}\n'.format(e2,e3,d4)
        j=mdc([e2,e3,d4])
        texto+='j = mdc({},{},{}) = {}\n'.format(e2,e3,d4,j)
        e6=e2//j
        e5=e3//j
        d5=d4//j
        texto+='{}k={}n+{}\n'.format(e6,e5,d5)
        if((e5%e6==0)and(d5%e6==0)):
            e8=e5//e6
            d8=d5//e6
        else:
            e7=e6
            right=False
            for d7 in range(e7):
                e8=e7*e5
                d8=e5*d7+d5
                if((e8%e6==0)and(d8%e6==0)):
                    texto+='{}k={}({}m+{})+{}\n'.format(e6,e5,e7,d7,d5)
                    right=True
                    break
            if(not(right)):
                texto+='contradiz\n\n'
                if(saida=='padrao'):
                    print(texto)
                else:
                    saida.write(texto)
                return(None)
        if(e6!=1):
            texto+='{}k={}n+{}\n'.format(e6,e8,d8)
            if((e8%e6==0)and(d8%e6==0)):
                e9=e8//e6
                d9=d8//e6
                e6=1
                texto+='{}k={}n+{}\n'.format(e6,e9,d9)
        else:
            e9=e8
            d9=d8
        texto+='x={}({}n+{})+{}\n'.format(e0,e9,d9,d0)
        e10=e0*e9
        d10=e0*d9+d0
        texto+='x={}n+{}\n\n'.format(e10,d10)
        if(saida=='padrao'):
            print(texto)
        else:
            saida.write(texto)
        return Formato(e10,d10)

    def setResto(self,novoResto):
        self.resto = self.testaResto(novoResto)

    def testaResto(self,novoResto):
        return int(novoResto)%self.divisor

    def copia(self):
        return Formato(self.divisor,self.resto)

    def puro(self):
        return [self.divisor,self.resto]
    
    def __str__(self):
        return self.textoSimples(self.varApresentacao)

class Formula:

    def __init__(self, a=1, b=0, c=1):
        if(str(type(a))=="<class 'list'>"):
            self.a=int(a[0])
            self.b=int(a[1])
            self.c=int(a[2])
        else:
            self.a=int(a)
            self.b=int(b)
            self.c=int(c)
        self.simplifica()
        self.varApresentacao='x'

    def numeroTeste(self,numero):
        return(((self.a*numero+self.b)%self.c)==0)

    def numeroValor(self,numero):
        if(self.numeroTeste(numero)):
            return (self.a*numero+self.b)//self.c
        else:
            return None

    def valor(self,x):
        return (self.a*x+self.b)/self.c

    def setVarApresentacao(self,letra):
        self.varApresentacao=str(letra)

    def textoSimples(self,x):
        texto=str(x)
        if(self.b!=0):
            if(self.b>0):
                texto+='+'+str(self.b)
            else:
                texto+=str(self.b)
            if(self.c!=1):
                texto+=')/'+str(self.c)
                if(self.a!=1):
                    return '('+str(self.a)+texto
                else:
                    return '('+texto
            else:
                if(self.a!=1):
                    return str(self.a)+texto
                else:
                    return texto
        else:
            if(self.c!=1):
                texto+='/'+str(self.c)
            if(self.a!=1):
                texto=str(self.a)+texto
            return texto

    def inversa(self):
        return Formula(self.c,-self.b,self.a)

    def aplica(self,outraFormula):
        newA=self.a*outraFormula.a
        newC=self.c*outraFormula.c
        newB=self.a*outraFormula.b+self.b*outraFormula.c
        return Formula(newA,newB,newC)

    def outFormato(self,inFormato):
        saidaFormato = inFormato.copia()
        saidaFormato.setDivisor((inFormato.divisor*self.a)//self.c)
        saidaFormato.setResto((inFormato.resto*self.a+self.b)//self.c)
        return saidaFormato

    def simplifica(self):
        j = mdc([self.a,self.b,self.c])
        self.a = self.a//j
        self.b = self.b//j
        self.c = self.c//j

    def copia(self):
        return Formula(self.a,self.b,self.c)

    def pura(self):
        return [self.a,self.b,self.c]
    
    def __str__(self):
        return self.textoSimples(self.varApresentacao)

class Regra:
    
    def __init__(self,formato=None,formula=None,tipo='ativa'):
        if(str(type(formato))=="<class 'list'>"):
            self.setFormato(formato[:2])
            self.setFormula(formato[2:])
        else:
            self.setFormato(formato)
            self.setFormula(formula)
        self.tipo=tipo

    def setFormula(self,formula):
        if(formula):
            if(str(type(formula))=="<class 'list'>"):
                self.formula = Formula(formula)
            else:
                self.formula = formula
        else:
            self.formula = Formula()

    def setFormato(self,formato):
        if(formato):
            if(str(type(formato))=="<class 'list'>"):
                self.formato = Formato(formato)
            else:
                self.formato = formato
        else:
            self.formato = Formato()

    def setTipo(self,novoTipo):
        self.tipo=novoTipo

    def getFormula(self):
        return self.formula.copia()

    def getFormato(self):
        a=self.formato
        return a.copia()

    def getTipo(self):
        return self.tipo

    def aplicaRegra(self, numero):
        return self.getFormula().valor(numero)

    def testaRegra(self, numero):
        return self.getFormato().numeroTeste(numero)

    def inversa(self):
        formulaRegra=self.getFormula()
        formatoRegra=self.getFormato()
        formatoInverso=formulaRegra.outFormato(formatoRegra)
        formulaInversa=formulaRegra.inversa()
        return Regra(formatoInverso,formulaInversa,self.tipo)

    def copia(self):
        return Regra(self.getFormato(),self.getFormula(),self.getTipo())

    def resolvePara(self,regra,saida='padrao'):
        formulaArg = self.getFormula()
        formatoArg = regra.getFormato()
        return self.getFormato().resolvePara(formatoArg,formulaArg,saida=saida)

    def pura(self):
        return self.getFormato().puro()+self.getFormula().pura()
    
    def __str__(self):
        return '{:20} : {:20}'.format(str(self.getFormato()),str(self.getFormula()))

class Funcao:

    def __init__(self,listaRegras=None):
        self.regras=[]
        self.regraQuant = 0
        if(listaRegras):
            for regra in listaRegras:
                self.addRegra(regra)

    def addRegra(self,regra,tipo=None):
        if(regra):
            if(str(type(regra))=="<class 'list'>"):
                if(not(tipo)):
                    tipo='normal'
                self.regras.append(Regra(regra,tipo=tipo))
            else:
                if(tipo):
                    regra.setTipo(tipo)
                self.regras.append(regra)
            self.regraQuant+=1

    def popRegra(self,index):
        if(index<self.regraQuant):
            self.regras.pop(index)
            self.regraQuant-=1

    def getRegra(self,index):
        if(index<self.regraQuant):
            return self.regras[index]

    def getRegras(self,tiposDados=None):
        tiposDados=tiposDados if tiposDados else []
        lista=[]
        for regra in self.regras:
            if(tiposDados):
                if(regra.getTipo() in tiposDados):
                    lista.append(regra.copia())
            else:
                lista.append(regra.copia())
        return lista

    def getTipos(self):
        lista=[]
        for regra in self.regras:
            tipo=regra.getTipo()
            if(tipo not in lista):
                lista.append(tipo)
        return lista

    def aplicaFuncao(self,x):
        lista=[]
        for regra in self.regras:
            if(regra.testaRegra(x)):
                lista.append(int(regra.aplicaRegra(x)))
        return lista

    def regrasAplicadasA(self,x):
        lista=[]
        for index,regra in enumerate(self.regras):
            if(regra.testaRegra(x)):
                lista.append(index)
        return lista

    def formatosRestantes(self):
        pass

    def copia(self):
        lista = []
        for regra in self.regras:
            lista.append(regra.copia())
        return Funcao(lista)

    def inversa(self):
        lista = []
        for regra in self.regras:
            lista.append(regra.inversa())
        return Funcao(lista)

    def passos(self,x):
        lista=[]
        while(x not in lista):
            aplicacao=self.aplicaFuncao(x)
            if(aplicacao):
                lista.append(x)
                x=aplicacao[0]
            else:
                lista=[]
                return lista
        lista.append(x)
        return lista

    def passosLoop(self,x):
        return len(self.passos(x))-1

    def valoresEmPassos(self,passos):
        funcaoInversa=self.inversa()
        novaLista=[1]
        for a in range(passos-1):
            lista=novaLista
            novaLista=[]
            for elemento in lista:
                novaLista+=funcaoInversa.aplicaFuncao(elemento)
        return(sorted(novaLista))

    def valoresEmPassosComLimites(self,passos,limite,inicio=1):
        lista=[]
        for a in range(inicio,limite+1):
            if(self.passosLoop(a)<=passos):
                lista.append(a)
        return(lista)

    def estruturaReal(self):
        funcaoReal = Funcao(self.getRegras(['principal','ativa']))
        return funcaoReal

    def estruturaUtil(self):
        funcaoUtil = Funcao(self.getRegras(['passiva']))
        return funcaoUtil

    def estruturaUtilFutura(self):
        funcaoUtil = Funcao(self.getRegras(['principal','passiva']))
        return funcaoUtil

    def salva(self,indice):
        BD = shelve.open('collatzRegras')
        lista=[]
        for tipo in self.getTipos():
            for regra in self.getRegras(tipo):
                lista.append([regra.pura(),tipo])
        BD['collatz{}'.format(indice)]=lista
        BD.close()

    def apresentacao(self,indice):
        texto=''
        index=0
        for tipo in self.getTipos():
            texto+='\n'+tipo+'\n\n'
            for regra in self.getRegras([tipo]):
                texto+='{:03d} : '.format(index)
                formato=regra.getFormato()
                texto+='2^{:02d}k+{}'.format(int(log(formato.divisor,2)),formato.resto)
                formula=regra.getFormula()
                texto+=' : {}'.format(index,str(regra))+"\n"
                index+=1
        return texto
    
    def __str__(self):
        texto=''
        index=0
        for tipo in self.getTipos():
            texto+='\n'+tipo+'\n\n'
            for regra in self.getRegras([tipo]):
                texto+='{:02d} : {}'.format(index,str(regra))+"\n"
                index+=1
        return texto

def Collatz(indice):
    BD = shelve.open('collatzRegras')
    collatz = Funcao()
    for regraSimples in BD['collatz{}'.format(indice)]:
        argumento=regraSimples[0]
        tipoArg=regraSimples[1]
        collatz.addRegra(argumento,tipo=tipoArg)
    BD.close()
    return collatz.copia()

def mdcC(lista):
    novaLista=[]
    for elemento in lista:
        if (elemento<0):
            novaLista.append(-elemento)
        elif(elemento>0):
            novaLista.append(elemento)      
    for d in range(min(novaLista),0,-1):
        cont=False
        for elemento in novaLista:
            if(elemento%d!=0):
                cont=True
        if(not(cont)):
            return(d)
    return(1)

def mdc(lista):
    novaLista=[]
    for elemento in lista:
        if (elemento<0):
            novaLista.append(-elemento)
        elif(elemento>0):
            novaLista.append(elemento)
    n2=0
    n3=0
    while True:
        cont=False
        for elemento in novaLista:
            if(elemento%(2**n2)!=0):
                cont=True
        if(not(cont)):
            n2+=1
        else:
            n2-=1
            break
    while True:
        cont=False
        for elemento in novaLista:
            if(elemento%(3**n3)!=0):
                cont=True
        if(not(cont)):
            n3+=1
        else:
            n3-=1
            break
    return((2**n2)*(3**n3))

if __name__ == '__main__':
    for a in range(7):
        print('\n\ncollatz {}\n\n'.format(a))
        print(Collatz(a))
    
