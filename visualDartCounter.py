#!/usr/bin/env python3
import cv2
import imutils
import numpy as np
import math


__version__ = "0.1" #Uitlezen van foto

global imageSize

def main():
    imageSize = 360
    dartboardPic = './images/dartboard_small.png'
    image = cv2.imread(dartboardPic, cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=imageSize)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    #Afbeelding blur
    '''
    convolutionKernel = np.ones((5, 5), np.float32) / 25
    blur = cv2.filter2D(imageHSV, -1, convolutionKernel)
    '''
    blur = cv2.blur(imgHSV, ksize=(5,5))

    # Opsplitsen op basis van HSV waarden: verder werken met de Value
    hImg, sImg, vImg = cv2.split(blur)

    #Afbeelding naar twee waarden converteren
    OTSUThreshVal, threshImg = cv2.threshold(vImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("thresh", threshImg)

    '''
    # removes border wire outside the outerellipse
    kernel = np.ones((5, 5), np.uint8)
    thresh2 = cv2.morphologyEx(threshImg, cv2.MORPH_CLOSE,kernel)
    
    cv2.imshow("thresh2", thresh2)
    '''

    edgedImg = cv2.Canny(threshImg, OTSUThreshVal, 0.5*OTSUThreshVal)
    cv2.imshow("canny", edgedImg)

    # Vind contouren op de afbeelding
    contours, hierarchy = cv2.findContours(threshImg, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        try:
            if imageSize*imageSize*0.25 < cv2.contourArea(cnt) < imageSize*imageSize:
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(image, ellipse, (0, 255, 0), cv2.LINE_4)

                x, y = ellipse[0] # center
                a, b = ellipse[1] # width, height
                angle = ellipse[2] # angle

                center_ellipse = (x, y)

                a = a/2
                b = b/2
        except:
            pass
        
    cv2.imshow("test_ellips", image)

    pointAreas(image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pointAreas(image):
    print("punten")

if __name__ == "__main__":
    main()