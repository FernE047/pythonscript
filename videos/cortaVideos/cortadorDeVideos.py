import subprocess


def main() -> None:
    subprocess.call(
        "ffmpeg -i C:/pythonscript/videos/videos/video0001.mp4 -r 24/1 -ss 00:00:50.0 -t 1 C:/pythonscript/videos/cortaVideos/frames/filename%04d.jpg"
    )


if __name__ == "__main__":
    main()