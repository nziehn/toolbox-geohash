from toolbox.geohash.lib import point as _uut

from nose import tools as _tools

import math as _math
from toolbox.geohash.lib import util as _util


def test_from_latlng():
    _tools.assert_equal(
        _uut.Point.from_latlng(lat=0, lng=0),
        _uut.Point(x=1, y=0, z=0)
    )

    _tools.assert_almost_equal(
        _uut.Point.from_latlng(lat=0, lng=90),
        _uut.Point(x=0, y=1, z=0)
    )

    _tools.assert_almost_equal(
        _uut.Point.from_latlng(lat=90, lng=90),
        _uut.Point(x=0, y=0, z=1)
    )

    _tools.assert_almost_equal(
        _uut.Point.from_latlng(lat=90, lng=0),
        _uut.Point(x=0, y=0, z=1)
    )

    _tools.assert_almost_equal(
        _uut.Point.from_latlng(lat=45, lng=0),
        _uut.Point(x=1, y=0, z=1).to_unit()
    )


def test_distance_along_great_circle():
    earth_circumference = _util.EARTH_RADIUS * 2 *_math.pi

    left = _uut.Point.from_latlng(lat=0, lng=0)
    right = _uut.Point.from_latlng(lat=90, lng=0)

    _tools.assert_almost_equal(
        left.distance_along_great_circle(right),
        earth_circumference / 4
    )

    right = _uut.Point.from_latlng(lat=45, lng=0)
    _tools.assert_almost_equal(
        left.distance_along_great_circle(right),
        earth_circumference / 8
    )

    right = _uut.Point.from_latlng(lat=0, lng=90)
    _tools.assert_almost_equal(
        left.distance_along_great_circle(right),
        earth_circumference / 4
    )

    left = _uut.Point.from_latlng(lat=45, lng=90)
    right = _uut.Point.from_latlng(lat=-45, lng=-90)
    _tools.assert_almost_equal(
        left.distance_along_great_circle(right),
        earth_circumference / 2
    )

    left = _uut.Point.from_latlng(lat=-45, lng=-90)
    right = _uut.Point.from_latlng(lat=45, lng=90)
    _tools.assert_almost_equal(
        left.distance_along_great_circle(right),
        earth_circumference / 2
    )