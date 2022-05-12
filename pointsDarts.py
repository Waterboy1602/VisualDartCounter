import cv2
import imutils
import numpy as np
from common import cart2pol, changeOrigin, pointInEllipse

def getPoints(dart, pointArea):
    doubleBuiten = pointArea["ellipses"][0]
    doubleBinnen = pointArea["ellipses"][1]
    trebleBuiten = pointArea["ellipses"][2]
    trebleBinnen = pointArea["ellipses"][3]
    bull = pointArea["ellipses"][4]
    bulleye = pointArea["ellipses"][5]

    rhoDartOriginBoard, phiDartOriginBoard = cart2pol(dart[0], dart[1])

    points = 0


    if not pointInEllipse(dart, doubleBuiten):
        pass
    elif pointInEllipse(dart, bull) and not pointInEllipse(dart, bulleye):
        points = 25
        pass
    elif pointInEllipse(dart, bulleye):
        points = 50
        pass
    else:
        double = False
        treble = False

        if pointInEllipse(dart, doubleBuiten) and not pointInEllipse(dart, doubleBinnen):
            double = True
        elif pointInEllipse(dart, trebleBuiten) and not pointInEllipse(dart, trebleBinnen):
            treble = True

        for i in range(20):
            if not i == 19:
                x, y = changeOrigin(pointArea["coordinaten"][i], pointArea["centerBord"])
                pointBorderOriginBoard1 = [x, y]
                x, y = changeOrigin(pointArea["coordinaten"][i+1], pointArea["centerBord"])
                pointBorderOriginBoard2 = [x, y]

                _, phiC = cart2pol(pointBorderOriginBoard1[0], pointBorderOriginBoard1[1])
                _, phiCC = cart2pol(pointBorderOriginBoard2[0], pointBorderOriginBoard2[1])
                if phiDartOriginBoard <= phiC and phiDartOriginBoard >= phiCC:
                    points = pointArea["punten"][i]
                    break
            else:
                x, y = changeOrigin(pointArea["coordinaten"][0], pointArea["centerBord"])
                pointBorderOriginBord0 = [x, y]
                _, phiC = cart2pol(pointBorderOriginBoard1[0], pointBorderOriginBoard1[1])
                _, phiCC = cart2pol(pointBorderOriginBord0[0], pointBorderOriginBord0[1])
                if phiDartOriginBoard <= phiC or phiDartOriginBoard >= phiCC:
                    points = pointArea["punten"][i]
        if double:
            points*=2
        elif treble:
            points*=3    
    return points