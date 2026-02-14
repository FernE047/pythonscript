import subprocess

SOURCE_VIDEO = "./input.mp4"
OUTPUT_TEMPLATE = "./video/frame_%03d.png"
FPS = 10


def main() -> None:
    subprocess.call(
        f"ffmpeg -i {SOURCE_VIDEO} -r {FPS}/1 {OUTPUT_TEMPLATE}", shell=True
    )


if __name__ == "__main__":
    main()
