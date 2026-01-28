import os

os.execl(
    "C:\\Program Files\\ffmpeg\\bin\\ffmpeg",
    "-f",
    "image2",
    "-r",
    "30",
    "-i",
    "C:\\camadas\\R\\a%d.jpg",
    "-vcodec",
    "libx264",
    "Rcolor.mp4",
)
raise exception
os.system(
    " ".join(
        [
            "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe ",
            "-f ",
            "image2 ",
            "-r ",
            "30 ",
            "-i ",
            "C:\\camadas\\R\\a%d.jpg ",
            "-vcodec ",
            "libx264 ",
            "Rcolor.mp4",
        ]
    )
)
