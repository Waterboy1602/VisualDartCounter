import cv2
import imutils
import numpy as np
import math
from common import lengteLijn, snijpuntLijn, afstandLijnPunt

def calibrate(imagePath):
    #!print("Calibrate")

    imageSize = 360
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
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

    diameter = 10e100
    for cnt in contours:
        try:
            if imageSize*imageSize*0.1 < cv2.contourArea(cnt) < imageSize*imageSize:
                ellipse = cv2.fitEllipse(cnt)
                cv2.ellipse(image, ellipse, (0, 255, 0), cv2.LINE_4)

                x, y = ellipse[0] # x- en y-coördinaat center
                a, b = ellipse[1] # grote as met halve lengte a, kleine as met halve lengte b ~ diameter
                angle = ellipse[2] # rotatiehoek

                center_ellipse = (x, y)

                diameter = min(diameter, a, b) # Binnenste cirkel (kleinste diameter) als er twee cirkels gevonden worden
        except:
            pass

    #cv2.imshow("test_ellips", image)

    # Vind sectie lijnen/grenzen
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 0.1*imageSize  # maximum gap in pixels between connectable line segments
    line_image = np.copy(image) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edgedImg, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    horizLines = []
    usefullLines = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            p1 = [x1, y1]
            p2 = [x2, y2]
            if lengteLijn(p1, p2) < 0.8*diameter: # Lengte lijnstuk 80% van de dartboard diameter bedraagt 
                continue
            if afstandLijnPunt((p1, p2), center_ellipse) > 0.15*imageSize: # Lijn voldoende dicht bij center
                continue
            usefullLines.append([x1,y1,x2,y2])

            cv2.line(line_image, (x1,y1), (x2,y2), (0,0,255), 3)

            hellingsgraad = math.atan((y2-y1)/(x2-x1))
            if hellingsgraad < np.pi/18 and hellingsgraad > -np.pi/18: # Horizontale lijnen zoeken
                horizLines.append([x1, y1, x2, y2])

    lines_edges = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    cv2.imshow("test_lines", lines_edges)

    if len(horizLines) >= 2:
        pointAreas(image, horizLines, usefullLines)
    elif len(horizLines) == 1:
        print("")
    else:
        print("")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pointAreas(image, horizLines, usefullLines):
    
    print("punten")