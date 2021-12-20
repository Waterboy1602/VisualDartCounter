import cv2
import imutils
import numpy as np
import math
import statistics

def recognizeDarts(imgBeforeThrowPath, imgAfterThrow):
    imageSize = 720
    imgBeforeThrow = cv2.imread(imgBeforeThrowPath, cv2.IMREAD_COLOR)
    imgBeforeThrow = imutils.resize(imgBeforeThrow, width=imageSize)
    imgBeforeThrowGray = cv2.cvtColor(imgBeforeThrow, cv2.COLOR_RGB2GRAY)

    imgAfterThrow = cv2.imread(imgAfterThrow, cv2.IMREAD_COLOR)
    imgAfterThrow = imutils.resize(imgAfterThrow, width=imageSize)
    imgAfterThrowGray = cv2.cvtColor(imgAfterThrow, cv2.COLOR_RGB2GRAY)



    frameDiff = cv2.absdiff(imgBeforeThrowGray, imgAfterThrowGray)

    #ToDo Uitleg in doc + verstaan
    blur = cv2.GaussianBlur(frameDiff, (5, 5), 0)
    blur = cv2.bilateralFilter(blur, 9, 75, 75)

    _, threshImg = cv2.threshold(frameDiff, 30, 200, cv2.THRESH_BINARY)

    cv2.imshow("frameDiff", frameDiff)
    cv2.imshow("thresh", threshImg)

    cv2.waitKey(0)  
    cv2.destroyAllWindows()

    return