import subprocess

diretorioVideo = "C:\\pythonscript\\imagem\\SpeedrunMapping\\video"
origemVideo = "-i C:\pythonscript\\imagem\\SpeedrunMapping\\level.mp4"
destinoTemp = diretorioVideo + "\\frame%02d.png"
fps = 10
extraArguments = "-r " + fps + "/1"
processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]
subprocess.call(" ".join(processoArgs))
