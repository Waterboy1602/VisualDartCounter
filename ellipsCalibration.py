import cv2
import imutils
import numpy as np
import math
import statistics

from common import lengthLine, distLinePoint, rotate

def calibrate(imagePath):
    imageSize = 360
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=imageSize)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Afbeelding blur
    blur = cv2.blur(imgHSV, ksize=(5,5))

    # Opsplitsen op basis van HSV waarden: verder werken met de Value
    _, _, vImg = cv2.split(blur)

    #Afbeelding naar twee waarden converteren
    OTSUThreshVal, threshImg = cv2.threshold(vImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow("thresh", threshImg)
    
    edgedImg = cv2.Canny(threshImg, OTSUThreshVal, 0.5*OTSUThreshVal)
    #cv2.imshow("canny", edgedImg)

    # Vind contouren op de afbeelding
    contours, _ = cv2.findContours(threshImg, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)

    diameter = 0
    omtrekBord = []
    for cnt in contours:
        try:
            if imageSize*imageSize*0.1 < cv2.contourArea(cnt) < imageSize*imageSize:
                ellipse = cv2.fitEllipse(cnt)

                x, y = ellipse[0] # x- en y-coördinaat center
                a, b = ellipse[1] # grote as met halve lengte a, kleine as met halve lengte b ~ diameter
                angle = ellipse[2] # rotatiehoek

                center_ellipse = (x, y)

                if a > diameter or b > diameter:
                    omtrekBord = ellipse

                diameter = max(diameter, a, b) # Buitenste cirkel (grootste diameter) als er meerdere cirkels gevonden worden    
        except:
            pass

    #cv2.ellipse(image, omtrekBord, (0, 255, 0), cv2.LINE_4)

    

    # Vind sectie lijnen/grenzen
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 0.15*imageSize  # maximum gap in pixels between connectable line segments
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
            if lengthLine(p1, p2) < 0.6*diameter: # Lengte lijnstuk 80% van de dartboard diameter bedraagt 
                continue
            if distLinePoint((p1, p2), center_ellipse) > 0.15*imageSize: # Lijn voldoende dicht bij center
                continue
            usefullLines.append([x1,y1,x2,y2])

            
            hellingsgraad = math.atan((y2-y1)/(x2-x1))
            if hellingsgraad < np.pi/18 and hellingsgraad > -np.pi/18: # Horizontale lijnen zoeken
                horizLines.append([x1, y1, x2, y2])
                cv2.line(line_image, (x1,y1), (x2,y2), (0,0,255), 3)

    lines_edges = cv2.addWeighted(image, 0.8, line_image, 1, 0)
    #cv2.imshow("test_lines", lines_edges)

    pointAreas = getPointAreas(image, horizLines, usefullLines, omtrekBord)

    cv2.imshow("punten", image)

    cv2.waitKey(0)  
    cv2.destroyAllWindows()
    
    return pointAreas

def getPointAreas(image, horizLines, usefullLines, omtrekBord):        
    centerBordX, centerBordY = omtrekBord[0]
    bordStraal = statistics.mean(omtrekBord[1]) / 2
    

    doubleBuitenStraal = bordStraal/225*170
    doubleBinnenStraal = bordStraal/225*162
    trebleBuitenstraal = bordStraal/225*107
    trebleBinnenStraal = bordStraal/225*99
    bullStraal = bordStraal/225*15.9
    bullEyeStraal = bordStraal/225*6.35

    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(doubleBuitenStraal), (0, 255, 0), thickness=1, lineType=8)
    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(doubleBinnenStraal), (0, 255, 0), thickness=1, lineType=8)
    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(trebleBuitenstraal), (0, 255, 0), thickness=1, lineType=8)
    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(trebleBinnenStraal), (0, 255, 0), thickness=1, lineType=8)
    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(bullStraal), (0, 255, 0), thickness=1, lineType=8)
    cv2.circle(image, (int(centerBordX), int(centerBordY)), int(bullEyeStraal), (0, 255, 0), thickness=1, lineType=8)

    straal = {"center":[centerBordX, centerBordY], "bord":bordStraal, 
            "doubleBuiten":doubleBuitenStraal, "doubleBinnen":doubleBinnenStraal, 
            "trebleBuiten":trebleBuitenstraal, "trebleBinnen":trebleBinnenStraal, 
            "bull":bullStraal, "bullEye":bullEyeStraal}

    puntVak = {}

    if len(horizLines) >=2:
        x10, y11 = 0, 0
        for point in horizLines:
            x10 = max(horizLines[0][0], horizLines[0][2], x10)
            y11 = max(horizLines[0][1], horizLines[0][3], y11)
        coordinaten = []
        segmentCirkel = 2 * math.pi / 20
        for i in range(20):
            x, y = rotate((centerBordX, centerBordY), (x10, y11), i*segmentCirkel)
            coordinaten.append([x, y])

        # Met de klok mee - [10] = 1ste lijn tussen 6/10
        puntVak[10] = coordinaten[0]
        puntVak[15] = coordinaten[1]
        puntVak[2] = coordinaten[2]
        puntVak[17] = coordinaten[3]
        puntVak[3] = coordinaten[4]
        puntVak[19] = coordinaten[5]
        puntVak[7] = coordinaten[6]
        puntVak[16] = coordinaten[7]
        puntVak[8] = coordinaten[8]
        puntVak[11] = coordinaten[9]
        puntVak[14] = coordinaten[10]
        puntVak[9] = coordinaten[11]
        puntVak[12] = coordinaten[12]
        puntVak[5] = coordinaten[13]
        puntVak[20] = coordinaten[14]
        puntVak[1] = coordinaten[15]
        puntVak[18] = coordinaten[16]
        puntVak[4] = coordinaten[17]
        puntVak[13] = coordinaten[18]
        puntVak[6] = coordinaten[19]
        
        for key in puntVak:
            cv2.line(image, (int(centerBordX), int(centerBordY)), (int(puntVak[key][0]), int(puntVak[key][1])), (0,0,255), 2)

    #ToDo als slechts 1 horizLine gevonden is
    if len(horizLines) == 1:
        pass

    punten = [10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6]

    #pointAreas = {"straal":straal, "punten":puntVak, "coordinaten":coordinaten}
    pointAreas = {"straal":straal, "punten":punten, "coordinaten":coordinaten}
    return pointAreas