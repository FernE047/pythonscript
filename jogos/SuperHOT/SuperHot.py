#! python3
# superHotEverything.py - Displays the mouse cursor"s current position.
import pyautogui
import msvcrt


def main() -> None:
    print("Press Ctrl-C to quit.")
    try:
        a = 0
        b = 0
        while True:
            if msvcrt.kbhit():
                if a == 0:
                    pyautogui.click(400, 400)
                    pyautogui.press("pause")
                    a = 1
                else:
                    if b:
                        pyautogui.click(400, 400)
                        b = 0
                    else:
                        pyautogui.click(1100, 400)
                        b = 1
            else:
                if a == 0:
                    a = 0
                else:
                    pyautogui.click(400, 400)
                    pyautogui.press("pause")
                    pyautogui.click(1100, 400)
                    a = 0
    except KeyboardInterrupt:
        print("\nDone.")

if __name__ == "__main__":
    main()