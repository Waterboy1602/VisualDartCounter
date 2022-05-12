#!/usr/bin/env python3
from roundCalibration import roundCalibrate
from ellipsCalibration import ellipsCalibrate
from pointsBlocks import point
from staticDarts import recognizeDarts, recognizeDarts2
from movingDarts import recognizeDartsCam
import pickle
from os import path

__version__ = "0.1" #Uitlezen van foto

def main():
    """ pointAreas = roundCalibrate("./images/dartboard.png")
    print("41")
    print("Totaal " + str(point("./images/dartboard_41.png", pointAreas)))
    print("75")
    print("Totaal " + str(point("./images/dartboard_75.png", pointAreas)))
    print("63")
    print("Totaal " + str(point("./images/dartboard_63.png", pointAreas)))
    print("46")
    print("Totaal " + str(point("./images/dartboard_46.png", pointAreas)))
    print("20")
    print("Totaal " + str(point("./images/dartboard_20.png", pointAreas)))
    """

    # pointAreas = roundCalibrate("./images/dartboard2.png")

    #pointAreas = ellipsCalibrate("./images/calibrateBoardAngle.png")
    if path.exists("pointArea"):
        with open('pointArea', 'rb') as pointAreas_file:
            pointArea = pickle.load(pointAreas_file)
    else:
        pointArea = ellipsCalibrate(1)
        with open('pointArea', 'wb') as pointAreas_file:
            pickle.dump(pointArea, pointAreas_file)

    # pointAreas = None
    # recognizeDarts2("./images/board_without_darts.png", "./images/board_with_darts")
    # recognizeDartsCam("./images/Darts_Thrown_Short.mp4", pointAreas)

    recognizeDartsCam(1, pointArea)



if __name__ == "__main__":
    main()