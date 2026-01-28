from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

def facialLandmarks(nome,detector,predictor):
    image = cv2.imread(nome)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rect = detector(gray, 1)[0]
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    return shape

def comparaFaces(nome1,nome2):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("C:\\pythonscript\\imagem\\projetoFaces\\shape_predictor_68_face_landmarks.dat")
    face1 = facialLandmarks(nome1,detector,predictor)
    face2 = facialLandmarks(nome2,detector,predictor)
    distancia = lambda ponto1,ponto2:((ponto1[0]-ponto2[0])**2+(ponto1[1]-ponto2[1])**2)**0.5
    maiorDistancia = distancia((0,0),(255,255))
    soma = sum([distancia(coord_1,coord_2)/maiorDistancia*100 for coord_1,coord_2 in zip(face1,face2)])
    return soma/68

nome = "C:\\pythonscript\\imagem\\projetoFaces\\faces\\alinhadas\\output{0:04d}.png"
print(comparaFaces(nome.format(0),nome.format(1)))
