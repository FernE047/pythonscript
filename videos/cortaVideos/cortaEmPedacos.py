import subprocess

subprocess.call(
    "ffmpeg -i C:\\pythonscript\\videos\\videos\\video0002.mp4 -ss 00:00:45.0 -codec copy -t 5 C:\\pythonscript\\videos\\videos\\videoCut1.mp4"
)
