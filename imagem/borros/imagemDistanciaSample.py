from PIL import Image
from colorsys import hsv_to_rgb

# TODO: there's something wrong with the hsv to rgb conversion here

CoordData = tuple[int, int]

MAX_BRIGHTNESS = 255
MAX_SIZE = MAX_BRIGHTNESS + 1
WHITE_HSV = (0, 0, 100)


def get_distance(point_a: CoordData, point_b: CoordData) -> float:
    distance_a = point_a[0] - point_b[0]
    distance_b = point_a[1] - point_b[1]
    distance = (distance_a**2 + distance_b**2) ** 0.5
    return distance


def generate_image(focus_point: CoordData, filename: str) -> None:
    image = Image.new("HSV", (MAX_SIZE, MAX_SIZE), WHITE_HSV)
    distance_from_focus = get_distance((0, 0), focus_point)
    for x in range(MAX_SIZE):
        for y in range(MAX_SIZE):
            current_distance = get_distance((x, y), focus_point)
            brightness = current_distance / distance_from_focus * MAX_BRIGHTNESS
            rgb_values = hsv_to_rgb(0, 0, brightness)
            pixel_rgb = tuple([int(color_component) for color_component in rgb_values])
            image.putpixel((x, y), pixel_rgb)
    image.save(filename)


def main() -> None:
    generate_image((255, 255), "pic1.png")
    generate_image((127, 127), "pic2.png")
    generate_image((185, 220), "pic3.png")


if __name__ == "__main__":
    main()
