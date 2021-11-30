import math
import numpy as np
from numpy.linalg import norm

def intersectLine(line1, line2): # snijpuntLijn((A, B), (C, D))
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    intersectX = det(d, xdiff) / div
    intersectY = det(d, ydiff) / div
    return intersectX, intersectY

def lengthLine(p1, p2):
    length = math.sqrt((p2[0]-p1[0])*(p2[0]-p1[0]) + (p2[1]-p1[1])*(p2[1]-p1[1]))
    return length

def distLinePoint(line, point):
    pointL1 = np.asarray(line[0])
    pointL2 = np.asarray(line[1])
    point = np.asarray(point)
    dist = norm(np.cross(pointL2-pointL1, pointL1-point))/norm(pointL2-pointL1)
    return dist

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    if phi < 0: # 0 < phi < 2pi 
        phi += (2*np.pi)
    return rho, phi

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y

def rotate(center, point, rad):
    centerX, centerY = center
    pointX, pointY = point

    x = centerX + math.cos(rad) * (pointX - centerX) - math.sin(rad) * (pointY - centerY)
    y = centerY + math.sin(rad) * (pointX - centerX) + math.cos(rad) * (pointY - centerY)
    return x, y

def changeOrigin(point, center):
    pointX, pointY = point
    centerX, centerY = center

    x = pointX - centerX
    y = centerY - pointY
    return x, y