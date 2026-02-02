#! python3
# perfectPokemon.py - plays pokemon
from PIL import Image
import pyautogui
import time
import random
import shelve


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
    print(sign + ", ".join(parts))

#menus
    
def save():
    pyautogui.click(20,40)
    espere()
    pyautogui.click(90,230)
    espere()
    pyautogui.click(330,260)
    espere()
    print("savo")

def load():
    pyautogui.click(20,40)
    espere()
    pyautogui.click(90,210)
    espere()
    pyautogui.click(330,260)
    espere()
    print("carregado")
    
def abrir():
    pyautogui.click(350,750)
    espere()
    pyautogui.click(81,41)
    espere()
    pyautogui.click(150,320)

def fim():
    pyautogui.click(350,750)
    pyautogui.click(900,600)

#procedimento de cutscenes
    
def inicio():
    global cores
    global teclas
    global BD
    espere(6)
    apertePor(enter)
    esperePor((554,170),(248,240,40))
    espere(2)
    apertePor(enter)
    ultimaConversa((67,104))
    conversaCompleta(12,(85,195))
    ultimaConversa((326,474))
    esperePor((600,70),(16,112,224))
    for x in range(7):
        apertePor(botaoA)
    apertePor(enter)
    ultimaConversa((85,120))
    setaVermelha(11)
    esperePor((467,330),(248,248,248)) #caminhao
    andePassos(direita,3)
    conversaCompleta(5,(289,494))
    espere()
    ultimaConversa((446,2))
    espere()
    conversaCompleta(4,(401,2))
    espere()
    andePassos(cima,5)
    transicao()
    andePassos(esquerda,2)
    andePassos(cima,1)
    apertePor(botaoA)
    conversaCompleta(1,(464,437))
    esperePor((100,100),(72,176,184))
    apertePor(botaoA)
    apertePor(cima)
    apertePor(botaoA)
    conversaCompleta(4,(607,2))
    espere(2)
    andePassos(direita,2)
    andePassos(cima,1)
    ultimaConversa((359,2))
    ultimaConversa((365,2))
    ultimaConversa((650,2))
    conversaCompleta(1,(175,2))
    conversaCompleta(2,(540,2))
    espere(2)
    caminhada([[direita,4],[baixo,4],0,[direita,9],[cima,1]])
    conversaCompleta(5,(570,445))
    andePassos(cima,6)
    transicao()
    caminhada([[baixo,2],[direita,3]])
    apertePor(botaoA)
    conversaCompleta(11,(506,447))
    espere(2)
    caminhada([[esquerda,3],[cima,3],0,[baixo,6],0,[esquerda,3],[cima,8]])
    conversaCompleta(3,(158,2))
    andePassos(cima,2)
    ultimaConversa((206,447))
    conversaCompleta(1,(362,2))
    caminhada([[esquerda,4],[cima,1]])
    apertePor(botaoA)
    espere(1)
    inicial=random.randint(0, 2)
    print(str(inicial))
    if(inicial==1):
        apertePor(direita)
        novoPokemon(nome="mudkip",level=5)
    elif(inicial==2):
        apertePor(esquerda)
        novoPokemon(nome="treecko",level=5)
    else:
        novoPokemon(nome="torchic",level=5)
    espere()
    apertePor(botaoA)
    apertePor(botaoA)
#BD

def limpaBD():
    global BD
    BD["ataques"]=[]
    BD["pokemons"]=[]
    BD["jogadorPokemons"]=[0,"","","","",""]
    BD["jogadorItens"]=[]
    BD.close()
    BD = shelve.open("C:/pythonscript/jogos/perfectGameplay/bd")

def colocaPokemon(slot,pokemon):
    global BD
    BD["jogadorPokemons"][slot]=procuraPokemon(pokemon)

def procuraPokemon(nome):
    global BD
    pokemons=BD["pokemons"]
    for indice in range(len(pokemons)):
        if nome==pokemons[indice]["nome"]:
            return(indice)

def tiraPokemon(slot):
    global BD
    BD["jogadorPokemons"][slot]=0

def novoPokemon(nome="",genero="f",level=0,nature="",typePKM="",HP=0,SPATK=0,SPDEF=0,attack=0,defense=9,speed=0,exp=0,nextExp=0,ataques=[]):
    global BD
    BD["pokemons"].append({"nome":nome,"genero":genero,"nature":nature,"level":level,"type":typePKM,"HP":HP,"SPATK":SPATK,"SPDEF":SPDEF,"attack":attack,"defense":defense,"speed":speed,"exp":exp,"nextExp":nextExp,"ataques":ataques})

def atualizaPokemon(indice,genero="",level=0,nature="",typePKM="",HP=0,SPATK=0,SPDEF=0,attack=0,defense=9,speed=0,exp=0,nextExp=0,ataques=[]):
    global BD
    pokemons=BD["pokemons"]
    if(level):
        pokemons[indice]["level"]=level
    if(genero):
        pokemons[indice]["genero"]=genero
    if(nature):
        pokemons[indice]["nature"]=nature
    if(typePKM):
        pokemons[indice]["typePKM"]=typePKM
    if(HP):
        pokemons[indice]["HP"]=HP
    if(SPATK):
        pokemons[indice]["SPATK"]=SPATK
    if(SPDEF):
        pokemons[indice]["SPDEF"]=SPDEF
    if(attack):
        pokemons[indice]["attack"]=attack
    if(defense):
        pokemons[indice]["defense"]=defense
    if(speed):
        pokemons[indice]["speed"]=speed
    if(exp):
        pokemons[indice]["exp"]=exp
    if(nextExp):
        pokemons[indice]["nextExp"]=nextExp
    if(ataques):
        pokemons[indice]["ataques"]=ataques
    BD["pokemons"]=pokemons

def verificaAtaque(ataqueVerifica):
    global BD
    ataques=BD["ataques"]
    for ataque in ataques:
        if ataque[0]==ataqueVerifica:
            return(ataque)
    ataques.append()

#esperas

def espere(secs=1/2,mensagem=True):
    if(mensagem):
        print("esperando "+str(secs)+" segundos")
    time.sleep(secs)
        
def esperePor(coordenadas,cor,pressed=0):
    print("esperando cor "+str(cor)+" nas coordenadas "+str(coordenadas))
    if(pressed):
        pyautogui.keyDown(pressed)
    while True:
        time.sleep(1/15)
        tela=pyautogui.screenshot()
        if(tela.getpixel(coordenadas)==cor):
            print("color found")
            if(pressed):
                pyautogui.keyUp(pressed)
            return()

def transicao():
    while True:
        time.sleep(1/15)
        tela=pyautogui.screenshot()
        if(tela.getpixel((367,276))==(248, 208, 176)):
            print("transicionado")
            time.sleep(1)
            return()

#conversas

def setaVermelha(step,vermelho=(224,8,8)):
    print("conversando")
    for x in range(step):
        pyautogui.keyDown("x")
        while True:
            sair=False
            tela=pyautogui.screenshot()
            for xCoord in range(65,705,10):
                if(tela.getpixel((xCoord,434))==vermelho):
                    pyautogui.keyUp("x")
                    apertePor("x",mensagem=False)
                    print("\ttecla x apertada "+str(x+1)+" vezes")
                    sair=True
                    break
                elif(tela.getpixel((xCoord,482))==vermelho):
                    pyautogui.keyUp("x")
                    apertePor("x",mensagem=False)
                    print("\ttecla x apertada "+str(x+1)+" vezes")
                    sair=True
                    break
            if(sair):
                break
    print("talking done")
    return()

def ultimaConversa(coordenadas):
    global cores
    if(coordenadas[1]==2):
        coordenadas=list(coordenadas)
        coordenadas[1]=495
        coordenadas=tuple(coordenadas)
    esperePor(coordenadas,cinzaMenu)
    apertePor("x")

def conversaCompleta(setas,coordenadas):
    setaVermelha(setas)
    ultimaConversa(coordenadas)

#andar e apertar

def apertePor(tecla,tempo=1/15,mensagem=True):
    if(mensagem):
        print("tecla "+tecla+" apertada")
    pyautogui.keyDown(tecla)
    time.sleep(tempo)
    pyautogui.keyUp(tecla)

def andePassos(direction,steps=1):
    print("andando para "+direction)
    for a in range(steps):
        apertePor(direction,tempo=1/300,mensagem=False)
        print("\t"+str(a+1)+" passos")
        time.sleep(1/3)
    print("andando terminado")

def caminhada(lista):
    for passos in lista:
        if(passos==0):
            transicao()
            continue
        andePassos(passos[0],passos[1])
    return()

#batalhas

def decifraFonte(numero):
    valores=("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","L")
    return(valores[numero-1])
    
class Inimigo():
    def __init__(self):
        scanNomeInimigo(self)
        self.genero = scanGeneroInimigo()
        self.vida   = scanVidaInimigo()

def scanNomeInimigo(inimigo):
    tela=pyautogui.screenshot()
    x=60
    nome=""
    cor=(64,64,64)
    while True:
        pixel=tela.getpixel((x,114))
        if(pixel==cor):
            imagem=Image.new("RGBA",(10,19),(255,255,255,255))
            for xLetra in range(10):
                for yLetra in range(19):
                    pixel=tela.getpixel((xLetra+x,yLetra+114))
                    if(pixel==cor):
                        imagem.putpixel((xLetra,yLetra),(0,0,0,255))
            for nomeArq in range(1,38):
                try:
                    comparada=Image.open("C:/pythonscript/jogos/perfectGameplay/alfabeto1/"+str(nomeArq)+".png")
                except:
                    comparada=False
                teste=False
                if(comparada):
                    teste=True
                    for xLetra in range(10):
                        for yLetra in range(19):
                            if(imagem.getpixel((xLetra,yLetra))!=comparada.getpixel((xLetra,yLetra))):
                                teste=False
                if teste:
                    break
            if not(teste):
                print(nome)
                print("qual o numero dessa letra?")
                nomeArq=int(input())
                imagem.save("C:/pythonscript/jogos/perfectGameplay/alfabeto1/"+str(nomeArq)+".png")
            nome+=decifraFonte(nomeArq)
            x+=10
        elif(x==315):
            break
        else:
            x+=1
    for letra in range(len(nome)-1,0,-1):
        if nome[letra]=="L":
            inimigo.nome=nome[:letra]
            inimigo.level=int(nome[letra+1:])
    return(nome)

def scanGeneroInimigo():
    tela=pyautogui.screenshot()
    for x in range(50,320):
        pixel=tela.getpixel((x,120))
        if(pixel==(114,203,224)):
            return("m")
        elif(pixel==(0,0,0)):
            return("f")
    return("f")

def scanVidaInimigo():
    tela=pyautogui.screenshot()
    cores=[(88,208,128),(200,168,8),(168,64,72)]
    vida=0
    for x in range(164,306):
        pixel=tela.getpixel((x,150))
        if(pixel in cores):
            vida+=1
    porcentagem=int(vida*100/142)
    return(porcentagem)

def atualizaVida(self):
    self.vida   = scanVidaInimigo()
    
def batalha():
    setaVermelha(1,vermelho=(248,0,0))
    esperePor((400,440),(72,64,80))
    inimigo=Inimigo()

def atualizaEmBatalha(slot):
    global teclas
    apertePor(baixo)
    apertePor(botaoA)
    espere(1)
    apertePor(botaoA)
    apertePor(botaoA)
    pokemon=lerInfo(slot)

def lerInfo(slot):
    global BD
    pokemons=BD["pokemons"]
    indice=BD["jogadorPokemons"][slot]
    tela=pyautogui.screenshot()
    
    return(slot)

vermelhoFala=(224,8,8)
cinzaMenu=(96,96,96)
cores=[vermelhoFala,cinzaMenu]
ataqueGlobal=[]
cima="i"
baixo="k"
esquerda="j"
direita="l"
enter="w"
botaoA="x"
botaoB="z"
teclas=[enter,botaoA,botaoB,cima,baixo,esquerda,direita]
BD = shelve.open("C:/pythonscript/jogos/perfectGameplay/bd")
limpaBD()
try:
    comeco=time.time()
    abrir()
    inicio()
    #load()
    setaVermelha(1,vermelho=(248,0,0))
    esperePor((400,440),(72,64,80))
    inimigo=Inimigo()
    print("batalhando com "+inimigo.nome)
    print("level "+str(inimigo.level))
    print("vida: "+str(inimigo.vida)+"%")
    atualizaEmBatalha(0)
    fim=time.time()
    tempo=fim-comeco
    print("completo em:")
    print_elapsed_time(tempo)
except KeyboardInterrupt:
    fim=time.time()
    tempo=fim-comeco
    print("completo em:")
    print_elapsed_time(tempo)
    print("\nDone.")
