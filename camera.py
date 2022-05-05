import cv2
import time
import imutils
import numpy as np

def filterCorners(corners):
    cornerdata = []
    tt = 0
    mean_corners = np.mean(corners, axis=0)
    for i in corners:
        xl, yl = i.ravel()
        # filter noise to only get dart arrow
        ## threshold important -> make accessible
        if abs(mean_corners[0][0] - xl) > 180:
            cornerdata.append(tt)
        if abs(mean_corners[0][1] - yl) > 120:
            cornerdata.append(tt)
        tt += 1

    corners_new = np.delete(corners, [cornerdata], axis=0)  # delete corners to form new array

    return corners_new


def recognizeDartsCam(videoPath):
    imageSize = 720

    cap = cv2.VideoCapture(videoPath)

    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    # Capture frame-by-frame 
    _, frame = cap.read()
    frame = imutils.resize(frame, width=imageSize)
    frameGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frameGrayLastDart = frameGray
    #time.sleep(0.1)

    minThresh = 1000
    maxThresh = 10000
    dartThrown = False

    while cap.isOpened():
        dartSec = 0
        ret, framePlus = cap.read()
        if not ret:
            break
        
        framePlus = imutils.resize(framePlus, width=imageSize)
        framePlusGray = cv2.cvtColor(framePlus, cv2.COLOR_RGB2GRAY)
        cv2.imshow("framePlus", framePlusGray)
        
        frameDiff = cv2.absdiff(frameGray, framePlusGray)

        #! Sleep toevoegen als met webcam
        #time.sleep(0.1)

        #ToDo Uitleg in doc + verstaan
        blur = cv2.GaussianBlur(frameDiff, (5, 5), 0)
        blur = cv2.bilateralFilter(blur, 9, 75, 75)

        _, threshImg = cv2.threshold(frameDiff, 30, 200, cv2.THRESH_BINARY)

        #print(cv2.countNonZero(threshImg))
        nonZero = cv2.countNonZero(threshImg)
        print(nonZero)
        cv2.imshow("threshImg", threshImg)

        timeAtThrow = time.time_ns()
        if nonZero > minThresh and nonZero < maxThresh and not dartThrown:
            #cv2.waitKey(0)

            # Fix for video (buffered)
            while True:
                 ret, framePlus = cap.read()
                 elapsedTime = time.time_ns() - timeAtThrow
                 if elapsedTime > 5000000:
                     break
            
            # When using cam
            #time.sleep(1.5)

            ret, framePlus = cap.read()
            framePlus = imutils.resize(framePlus, width=imageSize)
            framePlusGray = cv2.cvtColor(framePlus, cv2.COLOR_RGB2GRAY)

            frameDiff = cv2.absdiff(frameGrayLastDart, framePlusGray)

            #ToDo Uitleg in doc + verstaan
            blur = cv2.GaussianBlur(frameDiff, (5, 5), 0)
            blur = cv2.bilateralFilter(blur, 9, 75, 75)

            _, threshImg = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            cv2.imshow("threshImg", threshImg)

            cnts = cv2.findContours(threshImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            c = max(cnts, key=cv2.contourArea)

            right = tuple(c[c[:, :, 0].argmax()][0])

            dartThrown = True
            frameGrayLastDart = framePlusGray


            # goodFeaturesToTrack
            edges = cv2.goodFeaturesToTrack(threshImg, 640, 0.0008, 1, mask=None, blockSize=3, useHarrisDetector=1, k=0.06)  # k=0.08
            corners = np.int0(edges)

            filteredCorners = filterCorners(corners)
            # Iterate over the corners and draw a circle at that location
            threshImgFeatures = framePlus.copy()
            for i in filteredCorners:
                x,y = i.ravel()
                cv2.circle(threshImgFeatures,(x,y),4,(0,0,255),-1)
                
            # Display the image
            cv2.imshow('threshImgFeatures', threshImgFeatures)



            # Draw dots onto image
            cv2.drawContours(framePlus, [c], -1, (36, 255, 12), 1)
            cv2.circle(framePlus, right, 4, (0, 0, 255), -1)
            cv2.imshow("contour", framePlus)

            cv2.waitKey(0)

        if nonZero == 0 and dartThrown:
            dartThrown = False

        frameGray = framePlusGray

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()