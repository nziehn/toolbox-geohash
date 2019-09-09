import math as _math


EARTH_RADIUS = 6371


def rad2deg(x):
    return x * 360 / (2 * _math.pi)


def deg2rad(x):
    return x * 2 * _math.pi / 360


def angle(a, b):
    return _math.acos(a.dot(b) / a.length / b.length)