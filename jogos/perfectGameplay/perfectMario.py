#! python3
# superHotEverything.py - Displays the mouse cursor"s current position.
import pyautogui
import time


def pressFor(tecla, tempo=1):
    print(f"press {tecla}")
    pyautogui.keyDown(tecla)
    time.sleep(tempo)
    pyautogui.keyUp(tecla)


def main() -> None:
    try:
        pyautogui.click(340, 750)
        pyautogui.click(340, 500)
        time.sleep(1)
        pressFor("f7")
        pyautogui.typewrite("Super_mario_brothers.nst")
        pressFor("enter")
        time.sleep(2)
        pressFor("enter", 1)
        pressFor("l", 10)
        pyautogui.click(900, 600)
    except KeyboardInterrupt:
        print("\nDone.")


if __name__ == "__main__":
    main()