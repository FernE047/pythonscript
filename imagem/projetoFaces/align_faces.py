#v36
# import the necessary packages
import imutils
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import dlib
import cv2
import os

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor and the face aligner
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('C:\\pythonscript\\imagem\\projetoFaces\\shape_predictor_68_face_landmarks.dat')
fa = FaceAligner(predictor, desiredFaceWidth=256)

# load the input image, resize it, and convert it to grayscale
image = cv2.imread('C:\\pythonscript\\imagem\\projetoFaces\\faces\\originais\\pic0001.png')
image = imutils.resize(image, width=800)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# show the original input image and detect faces in the grayscale
# image
cv2.imshow("Input", image)
rects = detector(gray, 2)

nome = "C:\\pythonscript\\imagem\\projetoFaces\\faces\\alinhadas\\output{0:04d}.png"
# loop over the face detections
for rect in rects:
	# extract the ROI of the *original* face, then align the face
	# using facial landmarks
	(x, y, w, h) = rect_to_bb(rect)
	faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
	faceAligned = fa.align(image, gray, rect)
	# display the output images
	cv2.imshow("Original", faceOrig)
	cv2.imshow("Aligned", faceAligned)
	cv2.imwrite(nome.format(len(os.listdir("C:\\pythonscript\\imagem\\projetoFaces\\faces\\alinhadas"))),faceAligned)
	cv2.waitKey(0)


