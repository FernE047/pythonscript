import pyautogui
import time

coordsData = tuple[int, int]
colorData = tuple[int, int, int]

BLACK = (0, 0, 0)
LIGHT_GRAY = (240, 240, 240)
GRAY = (231, 232, 233)
DARK_GRAY = (59, 59, 59)
DARKER_GRAY = (19, 18, 18)
RED = (255, 0, 0)
BLUEISH = (132, 172, 221)
BLUE_GRAY = (216, 232, 245)
WINDOWS_BUTTON = (25, 750)
SEARCH = (100, 690)
WORD = (395, 150)
WORD_OPTION = (130, 150)
ALERT = (618, 500)
MACROS = (880, 570)
INSERT = (400, 150)
HEADER = (180, 30)
HEADER_OPTION = (690, 110)
HEADER_WAIT_1 = (1065, 188)
HEADER_WAIT_2 = (731, 188)
HEADER_OPTION_2 = (690, 210)
PAGE_NUMBER = (800, 110)
PAGE_NUMBER_WAIT = (802, 150)
PAGE_NUMBER_END = (800, 150)
PAGE_NUMBER_END_WAIT = (490, 255)
PAGE_NUMBER_END_OPTION = (500, 400)
DIFFERENT_FIRST_PAGE = (625, 60)
PAGE_LAYOUT = (260, 30)
ORIENTATION = (260, 110)
ORIENTATION_WAIT = (289, 136)
ORIENTATION_OPTION_1 = (260, 180)
EXIT_FOOTER = (130, 230)
BORDERS = (660, 70)
BORDERS_WAIT = (450, 170)
BORDERS_OPTION = (660, 500)
BORDERS_WINDOWS = (600, 550)
COLUMNS = (370, 110)
COLUMNS_WAIT = (420, 138)
CLOSE = (1330, 10)
ORIENTATION_OPTION_2 = (670, 400)
SCROLL_DOWN_WORD_AMOUNT = 39
PAGE_AMOUNT = 17
SLEEP_INTERVAL = 1


def wait_for(coords: coordsData, color: colorData) -> None:
    while True:
        pixel = pyautogui.screenshot().getpixel(coords)
        if pixel == color:
            return
        time.sleep(SLEEP_INTERVAL)


def click_and_wait(coords: coordsData, sleep_time: int = SLEEP_INTERVAL) -> None:
    pyautogui.click(coords)  # windows
    time.sleep(sleep_time)


def main() -> None:
    click_and_wait(WINDOWS_BUTTON)  # windows
    click_and_wait(SEARCH)  # search
    pyautogui.typewrite("word")  # type word
    wait_for(WORD, BLUEISH)
    click_and_wait(WORD_OPTION, 0)  # word
    wait_for(ALERT, LIGHT_GRAY)
    click_and_wait(MACROS)  # alert
    click_and_wait(INSERT)  # macros
    click_and_wait(HEADER)  # insert
    click_and_wait(HEADER_OPTION)  # header
    wait_for(HEADER_WAIT_1, GRAY)
    wait_for(HEADER_WAIT_2, DARKER_GRAY)
    click_and_wait(HEADER_OPTION_2)  # header/val croche
    click_and_wait(HEADER)  # insert
    click_and_wait(PAGE_NUMBER)  # page number
    wait_for(PAGE_NUMBER_WAIT, DARK_GRAY)
    click_and_wait(PAGE_NUMBER_END)  # page number/end of page
    wait_for(PAGE_NUMBER_END_WAIT, BLACK)
    click_and_wait(PAGE_NUMBER_END_OPTION)  # page number/end of page/option
    click_and_wait(DIFFERENT_FIRST_PAGE)  # different first page
    click_and_wait(PAGE_LAYOUT)  # page layout
    click_and_wait(ORIENTATION)  # orientation
    wait_for(ORIENTATION_WAIT, DARK_GRAY)
    click_and_wait(ORIENTATION_OPTION_1)  # orientation
    wait_for(EXIT_FOOTER, BLUE_GRAY)
    pyautogui.doubleClick(200, 170)  # exit footer
    click_and_wait(BORDERS)  # borders
    wait_for(BORDERS_WAIT, LIGHT_GRAY)
    click_and_wait(BORDERS_OPTION)  # borders
    wait_for(BORDERS_WINDOWS, RED)
    for _ in range(SCROLL_DOWN_WORD_AMOUNT):
        pyautogui.press("down")  # next page
    pyautogui.press("enter")  # next page
    for _ in range(PAGE_AMOUNT):
        pyautogui.press("enter")  # next page
    click_and_wait(COLUMNS)  # columns
    wait_for(COLUMNS_WAIT, DARK_GRAY)
    time.sleep(10 * SLEEP_INTERVAL)
    click_and_wait(CLOSE)  # close
    click_and_wait(ORIENTATION_OPTION_2)  # orientation


if __name__ == "__main__":
    main()
