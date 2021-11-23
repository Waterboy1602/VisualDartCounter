import cv2
import imutils
import numpy as np

def point(imagePath, puntenRegio):
    imageSize = 360
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    image = imutils.resize(image, width=imageSize)
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #HSV to array format
    h, s, v = 205, 100, 100
    h, s, v = h/2, (s/100)*255, (v/100)*255
    #hmin = 95, 255, 255
    #hmax= 179, 255, 255
    """ lower = np.array([95, 255, 255], dtype="uint8")
    upper = np.array([179, 255, 255], dtype="uint8") """

    # Probeersel
    lower = np.array([95, 255, 255], dtype="uint8")
    upper = np.array([179, 255, 255], dtype="uint8")

    img_blue = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("blue", img_blue)

    cv2.waitKey(0)
    cv2.destroyAllWindows()