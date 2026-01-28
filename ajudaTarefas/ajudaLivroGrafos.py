import pyautogui
import time

# it helps to automate the renaming and saving of images from books Grafos

for image_index in range(230, 314):
    for copy_index in range(2):
        user_input = input()
        pyautogui.click(340, 750)
        pyautogui.keyDown("ctrlleft")
        pyautogui.keyDown("shiftleft")
        pyautogui.press("x")
        pyautogui.keyUp("shiftleft")
        pyautogui.keyUp("ctrlleft")
        time.sleep(2)
        if (copy_index % 2) == 1:
            pyautogui.keyDown("ctrlleft")
            pyautogui.press("h")
            pyautogui.keyUp("ctrlleft")
        else:
            pyautogui.keyDown("ctrlleft")
            pyautogui.press("g")
            pyautogui.keyUp("ctrlleft")
        pyautogui.keyDown("ctrlleft")
        pyautogui.press("w")
        pyautogui.keyUp("ctrlleft")
        pyautogui.press("enter")
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.press("altleft")
        pyautogui.press("a")
        pyautogui.press("a")
        time.sleep(1)
        name = f"A{image_index + 1}"
        if copy_index == 0:
            name = f"{name}A"
        else:
            name = f"{name}B"
        name = f"{name}.jpg"
        pyautogui.typewrite(name)
        pyautogui.press("enter")
