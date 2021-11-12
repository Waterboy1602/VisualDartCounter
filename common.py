import math
import numpy as np
from numpy.linalg import norm

def snijpuntLijn(lijn1, lijn2): # snijpuntLijn((A, B), (C, D))
    xdiff = (lijn1[0][0] - lijn1[1][0], lijn2[0][0] - lijn2[1][0])
    ydiff = (lijn1[0][1] - lijn1[1][1], lijn2[0][1] - lijn2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*lijn1), det(*lijn2))
    snijX = det(d, xdiff) / div
    snijY = det(d, ydiff) / div
    return snijX, snijY

def lengteLijn(p1, p2):
    lengte = math.sqrt((p2[0]-p1[0])*(p2[0]-p1[0]) + (p2[1]-p1[1])*(p2[1]-p1[1]))
    return lengte

def afstandLijnPunt(lijn, punt):
    puntL1 = np.asarray(lijn[0])
    puntL2 = np.asarray(lijn[1])
    punt = np.asarray(punt)
    afstand = norm(np.cross(puntL2-puntL1, puntL1-punt))/norm(puntL2-puntL1)
    return afstand