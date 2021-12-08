import cv2
import imutils
import numpy as np
from common import cart2pol, changeOrigin

def point(imagePath, pointAreas):
    imageSize = 360
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=imageSize)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #HSV to array format
    h, s, v = 205, 100, 100
    h, s, v = h/2, (s/100)*255, (v/100)*255
    # Select the color blue
    lower = np.array([95, 255, 255], dtype="uint8")
    upper = np.array([179, 255, 255], dtype="uint8")

    img_blue = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("blue", img_blue)

    # Find contours on image
    contours, hierarchy = cv2.findContours(img_blue, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)
    dartLoc = []
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        dartLoc.append([x, y, w, h])
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)

    totalPoints=0

    for dart in dartLoc:
        middleD = [dart[0]+dart[2]/2, dart[1]+dart[3]/2] # Origin left top, positive axis runs down and right
        xD, yD = changeOrigin(middleD, pointAreas["straal"]["center"])
        middleDartOriginBord = [xD, yD]
        rhoDartOriginBoard, phiDartOriginBoard = cart2pol(middleDartOriginBord[0], middleDartOriginBord[1])
        
        points = 0
        if rhoDartOriginBoard > pointAreas["straal"]["bord"]:
            pass
        elif rhoDartOriginBoard < pointAreas["straal"]["bull"] and rhoDartOriginBoard > pointAreas["straal"]["bullEye"]:
            points = 25
            pass
        elif rhoDartOriginBoard < pointAreas["straal"]["bullEye"]:
            points = 50
            pass
        else:
            double = False
            treble = False

            if rhoDartOriginBoard < pointAreas["straal"]["doubleBuiten"] and rhoDartOriginBoard > pointAreas["straal"]["doubleBinnen"]:
                double = True
            elif rhoDartOriginBoard < pointAreas["straal"]["trebleBuiten"] and rhoDartOriginBoard > pointAreas["straal"]["trebleBinnen"]:
                treble = True

            for i in range(20):
                if not i == 19:
                    x, y = changeOrigin(pointAreas["coordinaten"][i], pointAreas["straal"]["center"])
                    pointBorderOriginBoard1 = [x, y]
                    x, y = changeOrigin(pointAreas["coordinaten"][i+1], pointAreas["straal"]["center"])
                    pointBorderOriginBoard2 = [x, y]

                    rhoC, phiC = cart2pol(pointBorderOriginBoard1[0], pointBorderOriginBoard1[1])
                    rhoCC, phiCC = cart2pol(pointBorderOriginBoard2[0], pointBorderOriginBoard2[1])
                    if phiDartOriginBoard <= phiC and phiDartOriginBoard >= phiCC:
                        points = pointAreas["punten"][i]
                        break
                else:
                    x, y = changeOrigin(pointAreas["coordinaten"][0], pointAreas["straal"]["center"])
                    pointBorderOriginBord0 = [x, y]
                    rhoC, phiC = cart2pol(pointBorderOriginBoard1[0], pointBorderOriginBoard1[1])
                    rhoCC, phiCC = cart2pol(pointBorderOriginBord0[0], pointBorderOriginBord0[1])
                    if phiDartOriginBoard <= phiC or phiDartOriginBoard >= phiCC:
                        points = pointAreas["punten"][i]

            if double:
                points*=2
            elif treble:
                points*=3    
        totalPoints+=points

    cv2.imshow("contour", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return totalPoints
