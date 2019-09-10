from toolbox.geohash.lib import util as _uut

from nose import tools as _tools

import math as _math
from toolbox.geohash.lib import point as _point


def test_rad2deg():
    _tools.assert_almost_equal(
        _uut.rad2deg(_math.pi),
        180
    )

    _tools.assert_almost_equal(
        _uut.rad2deg(_math.pi / 3),
        60
    )

    _tools.assert_almost_equal(
        _uut.rad2deg(_math.pi * 2),
        360
    )


def test_deg2rad():
    _tools.assert_almost_equal(
        _uut.deg2rad(180),
        _math.pi
    )

    _tools.assert_almost_equal(
        _uut.deg2rad(60),
        _math.pi / 3
    )

    _tools.assert_almost_equal(
        _uut.deg2rad(360),
        _math.pi * 2
    )


def test_angle():
    x1 = _point.Point(x=1, y=0, z=0)
    y1 = _point.Point(x=0, y=1, z=0)
    z1 = _point.Point(x=0, y=0, z=1)
    x1y1 = _point.Point(x=1, y=1, z=0)

    _tools.assert_almost_equal(
        _uut.angle(a=x1, b=y1),
        _math.pi / 2
    )

    _tools.assert_almost_equal(
        _uut.angle(a=x1, b=z1),
        _math.pi / 2
    )

    _tools.assert_almost_equal(
        _uut.angle(a=x1, b=x1y1),
        _math.pi / 4
    )