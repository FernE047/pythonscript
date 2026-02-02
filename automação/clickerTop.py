import pyautogui
import time

# automatic clicker with percentage display

time.sleep(5)
click_limit = 10**3
percentage_achieved = [0]
erase = 0
for current_click in range(1, click_limit + 1):
    pyautogui.click(780, 460)
    percentage = int(current_click / click_limit * 100)
    if percentage not in percentage_achieved:
        percentage_achieved.append(percentage)
        message = f"{percentage}%"
        print((erase * "\b") + message, end="", flush=True)
        erase = len(message)
input()  # just to pause the console at the end
print("\nDone!")