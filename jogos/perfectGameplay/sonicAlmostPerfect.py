#! python3
# superHotEverything.py - Displays the mouse cursor's current position.
import pyautogui
import time

def pressFor(tecla,tempo=1/15):
    print('press '+tecla)
    pyautogui.keyDown(tecla)
    time.sleep(tempo)
    pyautogui.keyUp(tecla)

def todosOsPress():
    pyautogui.click(340,750)
    time.sleep(1)
    pressFor('f8')

def visao(parametros):
    pixelColor=[0,0,0]
    pixelColor[0] = pyautogui.screenshot().getpixel((600, 500))
    pixelColor[1] = pyautogui.screenshot().getpixel((600, 400))
    pixelColor[2] = pyautogui.screenshot().getpixel((600, 300))
    if (pixelColor[0]==parametros[0]):
        if (pixelColor[1]==parametros[1]):
            if (pixelColor[2]==parametros[2]):
                return(pixelcolor)
            else:
                return(0)
        else:
            return(0)
    else:
        if (parametros[0]==0):
            return(pixelColor)
        else:
            return(0)
        
#X:640 Y:530
#X:10  Y:50
        
def waitFor(coordenadas,cor):
    while True:
        time.sleep(1/15)
        tela=pyautogui.screenshot()
        if(tela.getpixel(coordenadas)==cor):
            return()
        
try:
    pyautogui.click(350,750)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('tab')
    time.sleep(1/15)
    pyautogui.keyUp('tab')
    pyautogui.keyUp('ctrl')
    waitFor((316,289),(99,97,232))
    pyautogui.click(350,750)
    pyautogui.click(900,600)
except KeyboardInterrupt:
    print('\nDone.')
#o emulador não possui fps statico então sempre será aleatorio o caminho, logo não podemos descrever ações se não estabilizarmos o fps
