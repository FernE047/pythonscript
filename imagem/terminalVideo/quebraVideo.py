import os
import shutil

FRAMES_FOLDER = "./video"  # complete
VIDEO_NAME = "example.mp4"
OUTPUT_FOLDER = "./video2"
EXTENSION_USED = ".jpg"
FFMPEG_PATH = "ffmpeg"
FRAMES_TEMPLATE = f"thumb_%06d{EXTENSION_USED}"


def main() -> None:
    os.system(f"{FFMPEG_PATH} -i {VIDEO_NAME} {FRAMES_TEMPLATE} -hide_banner")
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
