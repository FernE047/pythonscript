from PIL import Image
from colorsys import hsv_to_rgb

CoordData = tuple[int, int]


def get_distance(point_a: CoordData, point_b: CoordData) -> float:
    distance_a = point_a[0] - point_b[0]
    distance_b = point_a[1] - point_b[1]
    distance = (distance_a**2 + distance_b**2) ** 0.5
    return distance


def fazImagem(focus_point: CoordData, file_name: str) -> None:
    image = Image.new("RGBA", (256, 256), (0, 0, 100))
    distance_from_focus = get_distance((0, 0), focus_point)
    for x in range(256):
        for y in range(256):
            current_distance = get_distance((x, y), focus_point)
            brightness = current_distance / distance_from_focus * 255
            rgb_values = hsv_to_rgb(0, 0, brightness)
            pixel_rgb = tuple([int(color_component) for color_component in rgb_values])
            image.putpixel((x, y), pixel_rgb)
    image.save(file_name)


def main() -> None:
    fazImagem((255, 255), "pic1.png")
    fazImagem((127, 127), "pic2.png")
    fazImagem((185, 220), "pic3.png")


if __name__ == "__main__":
    main()
