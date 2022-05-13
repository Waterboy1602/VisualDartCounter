import cv2
import imutils
import numpy as np
import math
import statistics

from common import lengthLine, distLinePoint, movePoint, rotate, intersectLine, intersectLineEllipse, degToRad, twoPointsToOne

# TODO fix ellips calibration
def ellipsCalibrate(imagePath):
    imageSize = 2048
    if not isinstance(imagePath, str):
        cap = cv2.VideoCapture(imagePath)

        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        # Capture frame-by-frame 
        _, originalImage = cap.read()
    else:
        originalImage = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    image = originalImage
    imageSize = image.shape[1] # width
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    blur = cv2.blur(imgHSV, ksize=(5,5))

    # Opsplitsen op basis van HSV waarden: verder werken met de Value
    _, _, vImg = cv2.split(blur)

    #Afbeelding naar twee waarden converteren
    OTSUThreshVal, threshImg = cv2.threshold(vImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # cv2.imshow("thresh", threshImg)

    edgedImg = cv2.Canny(threshImg, 200, 255)
    # cv2.imshow("canny", edgedImg)

    # Vind contouren op de afbeelding
    contours, _ = cv2.findContours(threshImg, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(threshImg, 1,  2)

    imageContour = image.copy()
    cv2.drawContours(imageContour, contours, -1, (0,255,0), 2)
    # cv2.imshow("contours", imageContour)

    
    diameter = float('inf')
    omtrekBord = []
    for cnt in contours:
        try:
            # if True:
            if imageSize*imageSize*0.1 < cv2.contourArea(cnt) < imageSize*imageSize:
            # if 0 < cv2.contourArea(cnt) < imageSize*500:
                ellipse = cv2.fitEllipse(cnt)
                # cv2.ellipse(image, ellipse, (0, 255, 0), thickness=2, lineType=8)

                x, y = ellipse[0] # x- en y-coördinaat center
                a, b = ellipse[1] # grote as met halve lengte a, kleine as met halve lengte b ~ diameter
                angle = ellipse[2] # rotatiehoek in graden

                centerEllipse = (x, y)

                if diameter == None:
                    omtrekBord = ellipse
                elif a < diameter or b < diameter:
                    omtrekBord = ellipse

                diameter = min(diameter, a, b) # Binnenste cirkel (kleinste diameter) als er meerdere cirkels gevonden worden. De cirkel met alle puntregio's in  
        except:
            pass
    
    # print("a: " + str(omtrekBord[1][0]) + "; b: " + str(omtrekBord[1][1]))
    # print("centerEllipse: " + str(omtrekBord[0]))

    cv2.ellipse(image, omtrekBord, (0, 255, 0), thickness=2, lineType=8)
    cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), thickness=1, lineType=8)
    # cv2.imshow("ellipse", image)

    lineImage = np.copy(image) * 0  # creating a blank to draw lines on
    # usefullLines, horizAndVertLines = getHoughLines(extrEdgedImg, lineImage, diameter, imageSize, centerEllipse)
    usefullLines, horizAndVertLines = getHoughLines(edgedImg, lineImage, diameter, imageSize, centerEllipse)

    # linesEdges = cv2.addWeighted(image, 0.8, lineImage, 1, 0)

    # cv2.imshow("lines", linesEdges)

    # Krijg center bord
    horizLine = [[horizAndVertLines[0][0][0], horizAndVertLines[0][0][1]],[horizAndVertLines[0][0][2], horizAndVertLines[0][0][3]]]
    vertLine = [[horizAndVertLines[1][0][0], horizAndVertLines[1][0][1]],[horizAndVertLines[1][0][2], horizAndVertLines[1][0][3]]]
    centerBoard_X, centerBoard_Y = intersectLine(horizLine, vertLine)
    cv2.circle(image, (int(centerBoard_X), int(centerBoard_Y)), 5, (0, 255, 0), thickness=1, lineType=8)


    lines_edges = cv2.addWeighted(image, 0.8, lineImage, 1, 0)
    cv2.imshow("test_lines", lines_edges)

    # Vind snijpunten
    circumference = [[]]
    for line in usefullLines:
        intersectPoints = intersectLineEllipse(line, omtrekBord)
        for point in intersectPoints:
            circumference[0].append(point)
            # cv2.circle(image, (int(point[0]), int(point[1])), 1, (0, 0, 255), thickness=4, lineType=8)
 
    # Verwijder punten die te dicht bij elkaar liggen
    for index1, point1 in enumerate(circumference[0]):
        for index2, point2 in enumerate(circumference[0]):
            if((lengthLine(point1, point2) < 15 and lengthLine(point1, point2) > 0 )):
                # print(lengthLine(point1, point2))
                del circumference[0][index2]
    
    for point in circumference[0]:
        cv2.circle(image, (int(point[0]), int(point[1])), 1, (0, 0, 255), thickness=4, lineType=8)



    # Sorteer punten op volgorde volgens richting cirkel (tegenrichting)
    nextIndex = 0
    pointFrom = [vertLine[0][0], vertLine[0][1]]
    newCircumference = []
    dist = float('inf')
    for i in range(len(circumference[0])):
        if i == 1: # Met de klok mee
            for index, pointTo in enumerate(circumference[0]):
                length = lengthLine(pointFrom, pointTo)
                if(length < dist and not pointFrom == pointTo and pointFrom[0] <  pointTo[0]):
                    dist = length
                    nextIndex = index
        else: 
            for index, pointTo in enumerate(circumference[0]):
                length = lengthLine(pointFrom, pointTo)
                if(length < dist and not pointFrom == pointTo):
                    dist = length
                    nextIndex = index
        dist = float('inf')
        pointFrom = circumference[0][nextIndex]
        newCircumference.append(pointFrom)
        del circumference[0][nextIndex]
        
    
    circumference[0] = newCircumference

    while(len(circumference[0]) > 20):
        for i in range(len(circumference[0])-1):
            # print(lengthLine(point1, point2))
            if(len(circumference[0])-i > 1):
                if(lengthLine(circumference[0][i], circumference[0][i+1]) < 25):
                    del circumference[0][i]

    # lol = originalImage.copy()
    # for i in range(len(circumference[0])):
        # cv2.line(lol, (int(centerBoard_X), int(centerBoard_Y)), (int(circumference[0][i][0]), int(circumference[0][i][1])), (0,0,255), 2)
        # cv2.imshow("LOL", lol)
        # cv2.waitKey(0)  
        # cv2.destroyAllWindows()
        
    # Bepaal overige punten
    # pointSegmentRadius = [160, 100, 90, 15.9, 6.35]
    pointSegmentRadius = [162, 107, 99, 15.9, 6.35]
    for segment in pointSegmentRadius:
        tempCircSegm= []
        for point in circumference[0]:        
            distance = segment/170
            resultX, resultY = movePoint(distance, (point, (centerBoard_X, centerBoard_Y)))
            cv2.circle(image, (int(resultX), int(resultY)), 1, (0, 0, 255), thickness=4, lineType=8)
            tempCircSegm.append((resultX, resultY))
        circumference.append(tempCircSegm)

    cv2.imshow("center", image)

    def onMouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('x = %d, y = %d'%(x, y))
    cv2.setMouseCallback('center', onMouse)

    # Vind overige ellipsen
    pointEllipses = []
    pointEllipses.append(omtrekBord)
    for pointsSegment in circumference[1:]:
        ellipse = cv2.fitEllipse(np.int32(pointsSegment))
        pointEllipses.append(ellipse)
        cv2.ellipse(image, ellipse, (0, 255, 0), thickness=2, lineType=8)
    cv2.imshow("newEllipse", image)


    pointLinesImg = originalImage.copy()
    pointArea = getPointArea(circumference, pointEllipses, (centerBoard_X, centerBoard_Y), pointLinesImg)
       
    cv2.waitKey(0)  
    cv2.destroyAllWindows()
    
    
    return pointArea

def getHoughLines(cannyImg, lineImage, diameter, imageSize, centerEllipse):
    ### HOUGHLINES
    lines = cv2.HoughLines(cannyImg, 1, np.pi / 180, 65, None, 0, 0)

    horizAndVertLines = [[], []]
    usefullLines = []
    if lines is not None:
        for line in lines:
            rho = line[0][0]
            theta = line[0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            p1 = [x1, y1]
            p2 = [x2, y2]
            if lengthLine(p1, p2) < 1*diameter: # Lengte lijnstuk 80% van de dartboard diameter bedraagt 
                continue
            if distLinePoint((p1, p2), centerEllipse) > 0.05*imageSize: # Lijn voldoende dicht bij center
                continue
            usefullLines.append([x1,y1,x2,y2])
            cv2.line(lineImage, (x1,y1), (x2,y2), (0,255,0), 3)

            # Horizontale en verticale lijnen zoeken
            if(x2-x1 == 0):
                hellingsgraad = np.pi/2
            else:
                hellingsgraad = math.atan((y2-y1)/(x2-x1))
            if (hellingsgraad < np.pi/18 and hellingsgraad > -np.pi/18): 
                horizAndVertLines[0].append([x1, y1, x2, y2])
                cv2.line(lineImage, (x1,y1), (x2,y2), (0,0,255), 3)
            if (hellingsgraad < np.pi/2 and hellingsgraad > np.pi*0.44):
                horizAndVertLines[1].append([x1, y1, x2, y2])
                cv2.line(lineImage, (x1,y1), (x2,y2), (0,0,255), 3)

    return usefullLines, horizAndVertLines

def getHoughLinesP(cannyImg, lineImage, diameter, imageSize, centerEllipse):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 0.25*imageSize  # maximum gap in pixels between connectable line segments
    lines = cv2.HoughLinesP(cannyImg, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    horizAndVertLines = []
    usefullLines = []
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                p1 = [x1, y1]
                p2 = [x2, y2]
                if lengthLine(p1, p2) < 1*diameter: # Lengte lijnstuk 80% van de dartboard diameter bedraagt 
                    continue
                if distLinePoint((p1, p2), centerEllipse) > 0.05*imageSize: # Lijn voldoende dicht bij center
                    continue
                usefullLines.append([x1,y1,x2,y2])
                cv2.line(lineImage, (x1,y1), (x2,y2), (0,0,255), 3)

                
                hellingsgraad = math.atan((y2-y1)/(x2-x1))
                if (hellingsgraad < np.pi/18 and hellingsgraad > -np.pi/18) or (hellingsgraad < np.pi/2 and hellingsgraad > np.pi*0.44): # Horizontale en verticale lijnen zoeken
                    horizAndVertLines.append([x1, y1, x2, y2])
                    cv2.line(lineImage, (x1,y1), (x2,y2), (0,0,255), 3)
    return usefullLines, horizAndVertLines

    
def getPointArea(circumference, pointEllipses, centerBord, image): 
    puntVak = []

    for index in range(20):
        puntVak.append(circumference[0][index])

    punten = [1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20]
    # punten= [12, 2, 16, 4, 1, 20, 7, 19, 18, 9, 5, 8, 13, 3, 17, 6, 15, 10, 11, 14]
    for index, value in enumerate(puntVak):
            # print(punten[index])
            cv2.line(image, (int(centerBord[0]), int(centerBord[1])), (int(value[0]), int(value[1])), (0,0,255), 2)
            cv2.imshow("Calibratie", image)

    pointArea = {"ellipses":pointEllipses, "punten":punten, "coordinaten":circumference[0], "centerBord":centerBord}
    return pointArea