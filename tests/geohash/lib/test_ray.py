from toolbox.geohash.lib import ray as _uut

from nose import tools as _tools

from toolbox.geohash.lib import point as _point


def test_ray():
    origin = _point.Point(x=0, y=0, z=0)
    x1 = _point.Point(x=1, y=0, z=0)
    x2y1 = _point.Point(x=2, y=1, z=0)

    ray1 = _uut.Ray(start=x1, end=x2y1)

    _tools.assert_equal(
        ray1.m,
        _point.Point(x=1, y=1, z=0)  # x2y1 - x1
    )

    _tools.assert_equal(
        ray1.b,
        x1
    )

    ray2 = _uut.Ray(start=origin, end=x2y1)

    _tools.assert_equal(
        ray2.m,
        _point.Point(x=2, y=1, z=0)  # x2y1
    )

    _tools.assert_equal(
        ray2.b,
        origin
    )

