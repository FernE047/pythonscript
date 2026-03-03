import pyautogui
import time

# this script was a silly attempt to make a perfect gameplay for mario, using an emulator. it doesn't work anymore because you need to have specific screen resolution and the game has to be in a specific position on the screen, but it was fun to make and it can be used as a base for other similar projects.

TIME_DEFAULT = 1.0
WINDOWS_MENU = (340, 750)
EMULATOR_POSITION = (340, 500)
MARIO_LEGAL_OBTAINED_ROM = "Super_mario_brothers.nst"
EXTRA_MENU_CLOSE = (900, 600)


def pressFor(key_to_press: str, time_to_press: float = TIME_DEFAULT) -> None:
    print(f"press {key_to_press}")
    pyautogui.keyDown(key_to_press)
    time.sleep(time_to_press)
    pyautogui.keyUp(key_to_press)


def click(coord: tuple[int, int]) -> None:
    x, y = coord
    print(f"clicking at {x}, {y}")
    pyautogui.click(x, y)


def main() -> None:
    try:
        click(WINDOWS_MENU)
        click(EMULATOR_POSITION)
        time.sleep(1)
        pressFor("f7")
        pyautogui.typewrite(MARIO_LEGAL_OBTAINED_ROM)
        pressFor("enter")
        time.sleep(2)
        pressFor("enter", 1)
        pressFor("l", 10)
        click(EXTRA_MENU_CLOSE)
    except KeyboardInterrupt:
        print("\nDone.")


if __name__ == "__main__":
    main()
