#!/usr/bin/env python3
from calibration import calibrate
from points import point


__version__ = "0.1" #Uitlezen van foto

def main():
    puntenregio = calibrate("./images/dartboard.png")
    print("41")
    print(point("./images/dartboard_41.png", puntenregio))
    print("57")
    print(point("./images/dartboard_57.png", puntenregio))
    print("66")
    print(point("./images/dartboard_66.png", puntenregio))


    puntenregio = calibrate("./images/dartboard2.png")

if __name__ == "__main__":
    main()