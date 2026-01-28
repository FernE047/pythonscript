#! python3
# superHotEverything.py - Displays the mouse cursor's current position.
import pyautogui
import msvcrt
import time

primeiroTempo = 15
segundoTempo = 30
print("Press Ctrl-C to quit.")
try:
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print(key)
            if str(key)[3] != "x":
                pyautogui.click(340, 750)
            if str(key)[2] == "x":
                time.sleep(1 / primeiroTempo)
                pyautogui.keyDown("x")
                time.sleep(1 / segundoTempo)
                pyautogui.keyUp("x")
            if str(key)[2] == "H":
                time.sleep(1 / primeiroTempo)
                pyautogui.keyDown("up")
                time.sleep(1 / segundoTempo)
                pyautogui.keyUp("up")
            if str(key)[2] == "P":
                time.sleep(1 / primeiroTempo)
                pyautogui.keyDown("down")
                time.sleep(1 / segundoTempo)
                pyautogui.keyUp("down")
            if str(key)[2] == "M":
                time.sleep(1 / primeiroTempo)
                pyautogui.keyDown("right")
                time.sleep(1 / segundoTempo)
                pyautogui.keyUp("right")
            if str(key)[2] == "K":
                time.sleep(1 / primeiroTempo)
                pyautogui.keyDown("left")
                time.sleep(1 / segundoTempo)
                pyautogui.keyUp("left")
            if str(key)[3] != "x":
                pyautogui.click(340, 750)
                time.sleep(1 / primeiroTempo)
                pyautogui.click(340, 750)
            pyautogui.click(1000, 350)
except KeyboardInterrupt:
    print("\nDone.")
