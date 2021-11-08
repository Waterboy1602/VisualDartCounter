#!/usr/bin/env python3
import cv2
import imutils
import numpy as np
import math


__version__ = "0.1" #Uitlezen van foto

def main():
    imageSize = 360
    dartboardPic = './images/dartboard.png'
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
    
    edgedImg = cv2.Canny(threshImg, OTSUThreshVal, 0.5*OTSUThreshVal)
    cv2.imshow("canny", edgedImg)

    # Vind contouren op de afbeelding
    contours, hierarchy = cv2.findContours(threshImg, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        try:
            if imageSize*imageSize*0.1 < cv2.contourArea(cnt) < imageSize*imageSize:
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

    # Vind sectie lijnen/grenzen
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(image) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edgedImg, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    #lines = cv2.HoughLines(edgedImg, 1, np.pi / 180, 100, 100)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

    lines_edges = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    cv2.imshow("test_lines", lines_edges)

    pointAreas(image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pointAreas(image):
    print("punten")

if __name__ == "__main__":
    main()