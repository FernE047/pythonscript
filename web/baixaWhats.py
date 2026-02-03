import pyautogui, time

#baixa do whatsapp web


def main() -> None:
    time.sleep(10)
    while(pyautogui.screenshot().getpixel((401, 299))!=(101, 56, 151)):
        time.sleep(1)
        pyautogui.click(1275, 100)
        time.sleep(1)
        pyautogui.click(1315, 355)


if __name__ == "__main__":
    main()