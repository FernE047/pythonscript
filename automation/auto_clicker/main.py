import pyautogui
import time

# automatic clicker with percentage display
CLICK_LIMIT = 10**3
INITIAL_DELAY = 5
CLICK_COORD = (780, 460)


def main() -> None:
    time.sleep(INITIAL_DELAY)
    percentage_achieved = [0]
    erase = 0
    for current_click in range(1, CLICK_LIMIT + 1):
        x, y = CLICK_COORD
        pyautogui.click(x, y)
        percentage = int(current_click / CLICK_LIMIT * 100)
        if percentage not in percentage_achieved:
            percentage_achieved.append(percentage)
            message = f"{percentage}%"
            print((erase * "\b") + message, end="", flush=True)
            erase = len(message)
    input()  # just to pause the console at the end
    print("\nDone!")


if __name__ == "__main__":
    main()
