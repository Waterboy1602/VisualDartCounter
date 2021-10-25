#!/usr/bin/env python3
import cv2
import imutils
import numpy as np


__version__ = "0.1" #Uitlezen van foto

def main():
    print("Start")


    dartboardPic = './images/dartboard_small.png'
    image = cv2.imread(dartboardPic, cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=360)
 
    imCalHSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    cv2.imshow("color", imCalHSV)
    cv2.waitKey(0)
    kernel = np.ones((5, 5), np.float32) / 25
    blur = cv2.filter2D(imCalHSV, -1, kernel)
    h, s, imCal = cv2.split(blur)
    ret, thresh = cv2.threshold(imCal, 140, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)

    # removes border wire outside the outerellipse
    kernel = np.ones((5, 5), np.uint8)
    thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel)
    cv2.imshow("thresh", thresh2)
    cv2.waitKey(0)
    # find enclosing ellipse
    #Ellipse, image_proc_img = findEllipse(thresh2,dartboardPic)

    img = cv2.imread(dartboardPic,0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,250,
                            param1=50,param2=30,minRadius=10,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    cv2.imshow('detected circles',cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()