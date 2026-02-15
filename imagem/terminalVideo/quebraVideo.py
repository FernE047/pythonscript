import os
import shutil

FRAMES_FOLDER = "./video"  # complete
VIDEO_NAME = "example"
OUTPUT_FOLDER = "./video2"
EXTENSION_USED = ".jpg"


def main() -> None:
    os.system(f"ffmpeg -i {VIDEO_NAME}.mp4 thumb_%06d{EXTENSION_USED} -hide_banner")
    print("Done, moving files...")
    frames_raw = os.listdir(FRAMES_FOLDER)
    frames = [f"{FRAMES_FOLDER}/{frame}" for frame in frames_raw]
    for frame in frames:
        _, extension = os.path.splitext(frame)
        if extension != EXTENSION_USED:
            continue
        shutil.move(frame, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
