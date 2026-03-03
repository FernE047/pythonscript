from typing import Literal
from PIL import Image
import pyautogui
import time

# this script was a silly attempt to make a perfect gameplay for sonic, using an emulator. it doesn't work anymore because you need to have specific screen resolution and the game has to be in a specific position on the screen, but it was fun to make and it can be used as a base for other similar projects.

TIME_DEFAULT = 1 / 15
EMULATOR_POSITION = (340, 500)
OPEN_WINDOWS_COLOR = (99, 97, 232)
WINDOWS_COLOR_TARGET = (316, 289)
SEE_DESKTOP_POSITION = (900, 600)


def pressFor(key_to_press: str, time_to_press: float = TIME_DEFAULT) -> None:
    print(f"press {key_to_press}")
    pyautogui.keyDown(key_to_press)
    time.sleep(time_to_press)
    pyautogui.keyUp(key_to_press)


def get_pixel(image: Image.Image, coord: tuple[int, int]) -> tuple[int, ...]:
    pixel = image.getpixel(coord)
    if pixel is None:
        raise ValueError("Pixel not found")
    if isinstance(pixel, int):
        raise ValueError("Image is not in RGB mode")
    if isinstance(pixel, float):
        raise ValueError("Image is not in RGB mode")
    if len(pixel) < 4:
        raise ValueError("Image is not in RGB mode")
    return pixel


def check_pixel_colors(  # never used.
    expected_pixel_colors: list[tuple[int, ...] | int],
) -> list[tuple[int, ...]] | Literal[0]:
    pixelColor: list[tuple[int, ...]] = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]
    pixelColor[0] = get_pixel(pyautogui.screenshot(), (600, 500))
    pixelColor[1] = get_pixel(pyautogui.screenshot(), (600, 400))
    pixelColor[2] = get_pixel(pyautogui.screenshot(), (600, 300))
    if pixelColor[0] != expected_pixel_colors[0]:
        if expected_pixel_colors[0] != 0:
            return 0
        return pixelColor
    if pixelColor[1] != expected_pixel_colors[1]:
        return 0
    if pixelColor[2] != expected_pixel_colors[2]:
        return 0
    return pixelColor


# X:640 Y:530
# X:10  Y:50


def waitFor(coord: tuple[int, int], color: tuple[int, int, int]) -> None:
    while True:
        time.sleep(TIME_DEFAULT)
        screen = pyautogui.screenshot()
        if get_pixel(screen, coord) == color:
            return


def click(coord: tuple[int, int]) -> None:
    x, y = coord
    print(f"clicking at {x}, {y}")
    pyautogui.click(x, y)


def main() -> None:
    try:
        click(EMULATOR_POSITION)
        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("tab")
        time.sleep(TIME_DEFAULT)
        pyautogui.keyUp("tab")
        pyautogui.keyUp("ctrl")
        waitFor(WINDOWS_COLOR_TARGET, OPEN_WINDOWS_COLOR)
        click(EMULATOR_POSITION)
        click(SEE_DESKTOP_POSITION)
    except KeyboardInterrupt:
        print("\nDone.")
    # the emulator doesn't have a static fps so the path will always be random, so we can't describe actions if we don't stabilize the fps
    # I never solved above problem, and this project is officially closed


if __name__ == "__main__":
    main()
