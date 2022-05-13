import math
import numpy as np
from numpy.linalg import norm
from sympy import Point, Line, Ellipse

def intersectLine(line1, line2): # snijpuntLijn((A, B), (C, D))
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    # xdiff = (line1[0] - line1[2], line2[0] - line2[2])
    # ydiff = (line1[1] - line1[3], line2[1] - line2[3])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    intersectX = det(d, xdiff) / div
    intersectY = det(d, ydiff) / div
    return intersectX, intersectY

def intersectLineEllipse(line, ellipse):
    rotRad = degToRad(ellipse[2])
    x0, y0, x1, y1 = line

    rx0, ry0 = rotate(ellipse[0], (x0, y0), -rotRad)
    rx1, ry1 = rotate(ellipse[0], (x1, y1), -rotRad)

    # return[(rx0, ry0), (rx1, ry1)]
    hradius, vradius = ellipse[1]
    hradius = hradius/2
    vradius = vradius/2
    el = Ellipse(Point(ellipse[0]), hradius, vradius)
    lineSegment = Line(Point(int(rx0), int(ry0)), Point(int(rx1), int(ry1)))
    result = el.intersection(lineSegment)
    points = []
    for point in result:
        points.append(rotate(ellipse[0], point, rotRad))
    return points


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
    x = np.float64(x)
    y = np.float64(y)
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

def degToRad(angle):
    return angle * np.pi/180

def radToDeg(angle):
    return angle * 180/np.pi

def movePoint(distance, line):
    x0, y0 = line[0]
    x1, y1 = line[1]
    resultX = distance * x0 + (1 - distance) * x1
    resultY = distance * y0 + (1 - distance) * y1
    return resultX, resultY

def twoPointsToOne(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    x3 = min(x1, x2) + abs(x1 - x2)
    y3 = min(y1, y2) + abs(y1 - y2)
    return x3, y3

def pointInEllipse(point, ellipse):
    x, y = ellipse[0]
    d, D = ellipse[1]
    angle = ellipse[2]

    xp, yp = point

    cosa = math.cos(angle)
    sina = math.sin(angle)
    dd = d/2 * d/2
    DD = D/2 * D/2

    a = math.pow(cosa*(xp-x)+sina*(yp-y),2)
    b = math.pow(sina*(xp-x)-cosa*(yp-y),2)
    ellipse = (a/dd) + (b/DD)

    if ellipse <= 1:
        return True
    else:
        return False