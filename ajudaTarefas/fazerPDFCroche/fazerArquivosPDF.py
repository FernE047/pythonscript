import pyautogui
import time

coordsData = tuple[int, int]
colorData = tuple[int, int, int]


def waitFor(coords: coordsData, color: colorData) -> None:
    while True:
        pixel = pyautogui.screenshot().getpixel(coords)
        if pixel == color:
            return
        time.sleep(1)


def clicaEspera(coords: coordsData, sleep_time: int = 1) -> None:
    pyautogui.click(coords)  # windows
    time.sleep(sleep_time)


def main() -> None:
    clicaEspera((25, 750))  # windows
    clicaEspera((100, 690))  # search
    pyautogui.typewrite("word")  # type word
    waitFor((395, 150), (132, 172, 221))
    clicaEspera((130, 150), 0)  # word
    waitFor((618, 500), (240, 240, 240))
    clicaEspera((880, 570))  # alert
    clicaEspera((400, 150))  # macros
    clicaEspera((180, 30))  # insert
    clicaEspera((690, 110))  # header
    waitFor((1065, 188), (231, 232, 233))
    waitFor((731, 188), (19, 18, 18))
    clicaEspera((690, 210))  # header/val croche
    clicaEspera((180, 30))  # insert
    clicaEspera((800, 110))  # page number
    waitFor((802, 150), (59, 59, 59))
    clicaEspera((800, 150))  # page number/end of page
    waitFor((490, 255), (0, 0, 0))
    clicaEspera((500, 400))  # page number/end of page/option
    clicaEspera((625, 60))  # different first page
    clicaEspera((260, 30))  # page layout
    clicaEspera((260, 110))  # orientation
    waitFor((289, 136), (59, 59, 59))
    clicaEspera((260, 180))  # orientation
    waitFor((130, 230), (216, 232, 245))
    pyautogui.doubleClick(200, 170)  # exit footer
    clicaEspera((660, 70))  # borders
    waitFor((450, 170), (240, 240, 240))
    clicaEspera((660, 500))  # borders
    waitFor((600, 550), (255, 0, 0))
    for _ in range(39):
        pyautogui.press("down")  # next page
    pyautogui.press("enter")  # next page
    for _ in range(17):
        pyautogui.press("enter")  # next page
    clicaEspera((370, 110))  # columns
    waitFor((420, 138), (59, 59, 59))
    # time.sleep(10)
    # clicaEspera((1330,10)) #close
    # clicaEspera((670,400)) #orientation


if __name__ == "__main__":
    main()
