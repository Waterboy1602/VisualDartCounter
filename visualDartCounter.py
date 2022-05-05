#!/usr/bin/env python3
from roundCalibration import calibrate
from points import point
from staticDarts import recognizeDarts, recognizeDarts2
from movingDarts import recognizeDartsCam


__version__ = "0.1" #Uitlezen van foto

def main():
    """ pointAreas = calibrate("./images/dartboard.png")
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

    pointAreas = calibrate("./images/dartboard2.png") """

    recognizeDarts2("./images/board_without_darts.png", "./images/board_with_darts")
    #recognizeDartsCam("./images/Darts_Thrown_Short.mp4")

if __name__ == "__main__":
    main()