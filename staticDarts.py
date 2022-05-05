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

    imgAfterThrow = str(imgAfterThrow) + ".png"
    print(imgAfterThrow)
    imgAfterThrow = cv2.imread(imgAfterThrow, cv2.IMREAD_COLOR)
    imgAfterThrow = imutils.resize(imgAfterThrow, width=imageSize)
    imgAfterThrowGray = cv2.cvtColor(imgAfterThrow, cv2.COLOR_RGB2GRAY)



    frameDiff = cv2.absdiff(imgBeforeThrowGray, imgAfterThrowGray)

    #ToDo Uitleg in doc + verstaan
    blur = cv2.GaussianBlur(frameDiff, (5, 5), 0)
    blur = cv2.bilateralFilter(blur, 9, 75, 75)

    _, threshImg = cv2.threshold(frameDiff, 30, 200, cv2.THRESH_BINARY)

    cnts = cv2.findContours(threshImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    c = max(cnts, key=cv2.contourArea)

    ## Obtain outer coordinates
    #left = tuple(c[c[:, :, 0].argmin()][0])
    #top = tuple(c[c[:, :, 1].argmin()][0])
    #bottom = tuple(c[c[:, :, 1].argmax()][0])
    right = tuple(c[c[:, :, 0].argmax()][0])

    print(right)
    # Draw dots onto image
    cv2.drawContours(imgAfterThrow, [c], -1, (36, 255, 12), 1)
    cv2.circle(imgAfterThrow, right, 4, (0, 0, 255), -1)


    cv2.imshow("frameDiff", frameDiff)
    cv2.imshow("thresh", threshImg)
    cv2.imshow("contour", imgAfterThrow)


    cv2.waitKey(0)  
    cv2.destroyAllWindows()

    return


def recognizeDarts2(imgBeforeThrowPath, imgAfterThrowPath):
    imageSize = 720
    imgBeforeThrow = cv2.imread(imgBeforeThrowPath, cv2.IMREAD_COLOR)
    imgBeforeThrow = imutils.resize(imgBeforeThrow, width=imageSize)
    imgBeforeThrowGray = cv2.cvtColor(imgBeforeThrow, cv2.COLOR_RGB2GRAY)

    for i in range(1,4):
        imgAfterThrow = str(imgAfterThrowPath) + "_" + str(i) + ".png"
        print(imgAfterThrow)
        imgAfterThrow = cv2.imread(imgAfterThrow, cv2.IMREAD_COLOR)
        imgAfterThrow = imutils.resize(imgAfterThrow, width=imageSize)
        imgAfterThrowGray = cv2.cvtColor(imgAfterThrow, cv2.COLOR_RGB2GRAY)



        frameDiff = cv2.absdiff(imgBeforeThrowGray, imgAfterThrowGray)

        #ToDo Uitleg in doc + verstaan
        blur = cv2.GaussianBlur(frameDiff, (5, 5), 0)
        blur = cv2.bilateralFilter(blur, 9, 75, 75)

        _, threshImg = cv2.threshold(frameDiff, 20, 500, cv2.THRESH_BINARY)

        cnts = cv2.findContours(threshImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        c = max(cnts, key=cv2.contourArea)

        ## Obtain outer coordinates
        #left = tuple(c[c[:, :, 0].argmin()][0])
        #top = tuple(c[c[:, :, 1].argmin()][0])
        #bottom = tuple(c[c[:, :, 1].argmax()][0])
        right = tuple(c[c[:, :, 0].argmax()][0])

        print(right)
        # Draw dots onto image
        cv2.drawContours(imgAfterThrow, [c], -1, (36, 255, 12), 1)
        cv2.circle(imgAfterThrow, right, 4, (0, 0, 255), -1)


        cv2.imshow("frameDiff", frameDiff)
        cv2.imshow("thresh", threshImg)
        cv2.imshow("contour", imgAfterThrow)


        cv2.waitKey(0)  
        cv2.destroyAllWindows()

        imgBeforeThrowGray = imgAfterThrowGray

    return