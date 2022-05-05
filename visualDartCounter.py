#!/usr/bin/env python3
from calibration import calibrate
from points import point
from darts import recognizeDarts


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
    recognizeDarts("./images/board_without_darts.png", "./images/board_with_darts.png")

if __name__ == "__main__":
    main()