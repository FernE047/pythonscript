from pathlib import Path
import shutil
import subprocess

FRAMES_FOLDER = Path("video")  # complete
VIDEO_NAME = "example.mp4"
OUTPUT_FOLDER = Path("video2")
EXTENSION_USED = ".jpg"
FFMPEG_PATH = "ffmpeg"
FRAMES_TEMPLATE = f"thumb_%06d{EXTENSION_USED}"


def turn_video_into_frames() -> None:
    subprocess.run([FFMPEG_PATH, "-i", VIDEO_NAME, FRAMES_TEMPLATE, "-hide_banner"])
    print("Done, moving files...")
    for frame in FRAMES_FOLDER.iterdir():
        if frame.suffix.lower() != EXTENSION_USED:
            continue
        shutil.move(frame, OUTPUT_FOLDER)
