print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
from utils import *
from sudoku import *
imgPath = "Resources/1.jpg"
imgHeight = 450
imgWidth = 450

#------------------------PREPARING IMAGE--------------------------------

img = cv2.imread(imgPath)
img = cv2.resize( img , (imgWidth, imgHeight))
imgBlank =   np.zeros((imgHeight,imgWidth,3) , np.uint8 )
imgThreshold = preProcess(img)
model = intializePredectionModel() 

#------------------------CONTOURS--------------------------------

imgContours = img.copy()
imgBigContours = img.copy()
contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 3) # DRAW ALL DETECTED CONTOURS


biggest, maxArea = biggestContour(contours) # FIND THE BIGGEST CONTOUR
biggest = reorder(biggest)
cv2.drawContours(imgBigContours,biggest,-1, (0, 255, 0), 3)
pts1 = np.float32(biggest)
pts2 =  np.float32([[0, 0],[imgWidth, 0], [0, imgHeight],[imgWidth, imgHeight]]) 
matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
imgWarpColored = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))
imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

imgDetectedDigits = imgBlank.copy()
imgSolvedDigits = imgBlank.copy()

boxes = splitBoxes(imgWarpColored)
# print(len(boxes))
# print(boxes[0].shape)
numbers = getPredection(boxes, model)
# print(numbers)
# print( type(numbers))
imgDetectedDigits = displayNumbers(imgDetectedDigits, numbers, color=(255, 0, 255))
numbers = np.asarray(numbers)
posArray = np.where(numbers > 0, 0, 1)

board = np.array_split(numbers,9)
solver(board)
flatList = []
for sublist in board:
    for item in sublist:
        flatList.append(item)
solvedNumbers =flatList*posArray
imgSolvedDigits= displayNumbers(imgSolvedDigits,solvedNumbers)
pts2 = np.float32(biggest) # PREPARE POINTS FOR WARP
pts1 =  np.float32([[0, 0],[imgWidth, 0], [0, imgHeight],[imgWidth, imgHeight]]) # PREPARE POINTS FOR WARP
matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GER
imgInvWarpColored = img.copy()
imgInvWarpColored = cv2.warpPerspective(imgSolvedDigits, matrix, (imgWidth, imgHeight))
inv_perspective = cv2.addWeighted(imgInvWarpColored, 1, img, 0.5, 1)
imgDetectedDigits = drawGrid(imgDetectedDigits)
imgSolvedDigits = drawGrid(imgSolvedDigits)
imageArray = ([img,imgThreshold,imgContours, imgContours],
              [inv_perspective, imgSolvedDigits,imgDetectedDigits,imgBlank])
stackedImage = stackImages(imageArray, 1)
cv2.imshow('Stacked Images', stackedImage)
cv2.waitKey(0)