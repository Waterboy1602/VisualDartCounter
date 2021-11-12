#!/usr/bin/env python3
from calibration import calibrate


__version__ = "0.1" #Uitlezen van foto

def main():
    calibrate("./images/dartboard.png")
    calibrate("./images/dartboard2.png")
    calibrate("./images/dartboard3.png")

if __name__ == "__main__":
    main()