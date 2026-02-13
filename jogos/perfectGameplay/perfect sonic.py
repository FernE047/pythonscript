#! python3
# superHotEverything.py - Displays the mouse cursor"s current position.
import pyautogui
import time


def pressFor(tecla, tempo=1 / 15):
    print(f"press {tecla}")
    pyautogui.keyDown(tecla)
    time.sleep(tempo)
    pyautogui.keyUp(tecla)


def todosOsPress():
    pyautogui.click(340, 750)
    time.sleep(1)
    pressFor("f8")


def visao(parametros):
    pixelColor = [0, 0, 0]
    pixelColor[0] = pyautogui.screenshot().getpixel((600, 500))
    pixelColor[1] = pyautogui.screenshot().getpixel((600, 400))
    pixelColor[2] = pyautogui.screenshot().getpixel((600, 300))
    if pixelColor[0] == parametros[0]:
        if pixelColor[1] == parametros[1]:
            if pixelColor[2] == parametros[2]:
                return pixelcolor
            else:
                return 0
        else:
            return 0
    else:
        if parametros[0] == 0:
            return pixelColor
        else:
            return 0


def esseTempo(tecla, tempo):
    todosOsPress()
    pressFor(tecla, tempo / 15)
    parametros = visao([0, 0, 0])
    b = 1
    for a in range(5):
        todosOsPress()
        pressFor(tecla, tempo / 15)
        if visao(parametros) == 0:
            return 0
    return 1


def quantoTempo(tecla):
    i = 0
    velho = 1
    novo = 1
    while True:
        velhoi = i
        i = i + 1
        velho = novo
        print(f"testando {tecla} por {i}/15")
        novo = esseTempo(tecla, i)
        if velho != novo:
            return velhoi


def main() -> None:
    try:
        tecla = "l"
        tempofinal = quantoTempo(tecla)
        print(f"tempo final foi {tempofinal}")
        print(f"adicione \npressFor({tecla});")
        pyautogui.click(900, 600)
    except KeyboardInterrupt:
        print("\nDone.")
    # o emulador não possui fps statico então sempre será aleatorio o caminho, logo não podemos descrever ações se não estabilizarmos o fps


if __name__ == "__main__":
    main()