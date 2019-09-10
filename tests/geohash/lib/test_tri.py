from toolbox.geohash.lib import tri as _uut

from nose import tools as _tools

import math as _math
from toolbox.geohash.lib import point as _point


def test_area_on_sphere():
    points = [
        _point.Point.from_latlng(lat=0, lng=0),
        _point.Point.from_latlng(lat=0, lng=90),
        _point.Point.from_latlng(lat=90, lng=0),
    ]
    triangle = _uut.Tri(*points)

    area_on_sphere = triangle.area_on_sphere()
    total_area_on_sphere = 4 * _math.pi * 1

    _tools.assert_almost_equal(
        area_on_sphere,
        total_area_on_sphere / 8
    )