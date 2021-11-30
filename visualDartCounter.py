#!/usr/bin/env python3
from calibration import calibrate
from points import point


__version__ = "0.1" #Uitlezen van foto

def main():
    puntenregio = calibrate("./images/dartboard.png")
    print("41")
    print("Totaal " + str(point("./images/dartboard_41.png", pointAreas)))
    print("75")
    print("Totaal " + str(point("./images/dartboard_75.png", pointAreas)))
    print("63")
    print("Totaal " + str(point("./images/dartboard_63.png", pointAreas)))


    puntenregio = calibrate("./images/dartboard2.png")

if __name__ == "__main__":
    main()