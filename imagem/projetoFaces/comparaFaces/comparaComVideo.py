# v36
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
from send2trash import send2trash
from imutils import face_utils
from os import listdir
from os import remove
from time import time
import numpy as np
import subprocess
import imutils
import dlib
import cv2


def embelezeTempo(segundos: float) -> str:
    if segundos < 0:
        segundos = -segundos
        sign = "-"
    else:
        sign = ""
    total_ms = int(round(segundos * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_min = total_s // 60
    m = total_min % 60
    total_h = total_min // 60
    h = total_h % 24
    d = total_h // 24
    parts: list[str] = []

    def add(value: int, singular: str, plural: str) -> None:
        if value:
            parts.append(f"{value} {singular if value == 1 else plural}")

    add(d, "day", "days")
    add(h, "hour", "hours")
    add(m, "minute", "minutes")
    add(s, "second", "seconds")
    if ms or not parts:
        parts.append(f"{ms} millisecond" if ms == 1 else f"{ms} milliseconds")
    return sign + ", ".join(parts)


def capturaFaces(nome):
    global DETECTOR
    global PREDICTOR
    global FA
    image = cv2.imread(nome)
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = DETECTOR(gray, 1)
    nome = "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces\\face{0:04d}.png"
    for rect in rects:
        indice = len(
            listdir("C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces")
        )
        faceAligned = FA.align(image, gray, rect)
        cv2.imwrite(nome.format(indice), faceAligned)
        cv2.imwrite(nome.format(indice + 1), cv2.flip(faceAligned, 1))


def facialLandmarks(nome):
    global DETECTOR
    global PREDICTOR
    image = cv2.imread(nome)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rect = DETECTOR(gray, 1)
    if rect:
        shape = face_utils.shape_to_np(PREDICTOR(gray, rect[0]))
    else:
        shape = []
    return shape


def comparaFaces(face1, nome2):
    face2 = facialLandmarks(nome2)
    if face2 == []:
        return 100
    distancia = (
        lambda ponto1, ponto2: (
            (ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2
        )
        ** 0.5
    )
    maiorDistancia = distancia((0, 0), (255, 255))
    soma = sum(
        [
            distancia(coord_1, coord_2) / maiorDistancia * 100
            for coord_1, coord_2 in zip(face1, face2)
        ]
    )
    return soma / 68


# Constantes:
nome = f"C:\\pythonscript\\imagem\\projetoFaces\\faces\\alinhadas\\output{0:04d}.png"
DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor(
    "C:\\pythonscript\\imagem\\projetoFaces\\shape_predictor_68_face_landmarks.dat"
)
FA = FaceAligner(PREDICTOR, desiredFaceWidth=256)
faceOriginal = facialLandmarks(nome)

# duracao arredondada em minutos do video
segundos = 9
minutos = 0
horas = 0


# Argumentos do FFMPEG
origemVideo = "-i C:\pythonscript\\imagem\\projetoFaces\\comparaFaces\\aim.mp4"  #'-i C:\\pythonscript\\videos\\videos\\video0002.mp4'
destinoTemp = (
    "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFrames\\frame%04d.png"
)
extraArguments = "-r 24/1 -ss {0:02d}:{1:02d}:{2:02d}.0 -t 1"
processoArgs = ["ffmpeg", origemVideo, extraArguments, destinoTemp]

# iniciadores
maiorDiferenca = 100
inicio = time()
inicioFirst = time()
first = True

for hora in range(horas + 1):
    for minuto in range(minutos + 1):
        for segundo in range(segundos + 1):
            processoArgs[2] = extraArguments.format(hora, minuto, segundo)
            subprocess.call(" ".join(processoArgs))
            for frame in listdir(
                "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFrames"
            ):
                capturaFaces(
                    "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFrames\\"
                    + frame
                )
                remove(
                    "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFrames\\"
                    + frame
                )
                # send2trash('C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFrames\\'+frame)
            for face in listdir(
                "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces"
            ):
                diferenca = comparaFaces(
                    faceOriginal,
                    "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces\\"
                    + face,
                )
                if diferenca < maiorDiferenca:
                    print(f"{hora:02d}:{minuto:02d}:{segundo:02d}.0")
                    print(maiorDiferenca)
                    print()
                    maiorDiferenca = diferenca
                    cv2.imwrite(
                        "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\perfectFrame.png",
                        cv2.imread(
                            "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces\\"
                            + face
                        ),
                    )
                remove(
                    "C:\\pythonscript\\imagem\\projetoFaces\\comparaFaces\\tempFaces\\"
                    + face
                )
            if first:
                finalFirst = time()
                duracao = finalFirst - inicioFirst
                first = False
                print(
                    "o processo completo demorará em média : "
                    + embelezeTempo(
                        duracao * (segundos + minutos * 60 + horas * 60 * 60)
                    )
                )
                finalFirst, inicioFirst, duracao = [None, None, None]
            if maiorDiferenca == 0:
                break
        if maiorDiferenca == 0:
            break
    if maiorDiferenca == 0:
        break
final = time()
duracao = final - inicio
print("o processo completo demorou : " + embelezeTempo(duracao))
