import os
import shutil

nome=input()
video=nome+".mp4""
os.system("ffmpeg -i "+video+" thumb%06d.jpg -hide_banner")
print("baixado")
directory = "" #complete
frames=[os.path.join(directory,frame) for frame in os.listdir(os.path.join(directory))]
for frame in frames:
    if(frame[1][-4:]==".jpg"):
        shutil.move(frame,os.path.join("C:\\","pythonscript","terminalVideo","video2"))
