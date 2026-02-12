import subprocess


def main() -> None:
    origemVideo = "-i ./level.mp4"
    destinoTemp = "./video/frame%02d.png"
    fps = 10
    extraArguments = f"-r {fps}/1"
    processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]
    subprocess.call(" ".join(processoArgs))


if __name__ == "__main__":
    main()