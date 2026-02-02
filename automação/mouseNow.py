import pyautogui
import msvcrt


def turn_color_to_string(color: tuple[int, int, int]) -> str:
    color_list = ", ".join([f"{str(rgb_value).rjust(3)}" for rgb_value in color])
    return f"RGB: ({color_list})"


print("Press Ctrl-C to quit.")
try:
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print(key)
        x, y = pyautogui.position()
        color_captured = pyautogui.screenshot().getpixel((x, y))
        if color_captured is None:
            continue
        pixel_color = (0, 0, 0)
        if isinstance(color_captured, float) or isinstance(color_captured, int):
            pixel_color = (
                int(color_captured),
                int(color_captured),
                int(color_captured),
            )
        else:
            if len(color_captured) <= 3:
                continue
            pixel_color = (color_captured[0], color_captured[1], color_captured[2])
        text = f"X: {str(x).rjust(4)} Y: {str(y).rjust(4)} {turn_color_to_string(pixel_color)}"
        print(text, end="")
        print("\b" * len(text), end="", flush=True)
except KeyboardInterrupt:
    print("\nDone.")
