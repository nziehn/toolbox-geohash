from toolbox import geohash as _uut

from nose import tools as _tools

from toolbox.geohash.lib import point as _point


def test_encode_icosahedron():
    geohash = _uut.Geohash(area_in_km_square=100 * 1000)

    _tools.assert_equal(
        geohash.encode(lat=0, lng=0),
        4304
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=45),
        909
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=90),
        594
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=-90),
        1362
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=270),
        1362
    )

    _tools.assert_equal(
        geohash.encode(lat=-87, lng=127),
        2510
    )

    _tools.assert_equal(
        geohash.encode(lat=17, lng=-42),
        1689
    )


def test_encode_tetrahedron():
    geohash = _uut.Geohash(area_in_km_square=100 * 1000, sphere_approx=_uut.TETRAHEDRON)

    _tools.assert_equal(
        geohash.encode(lat=0, lng=0),
        1350
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=45),
        819
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=90),
        1016
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=-90),
        311
    )

    _tools.assert_equal(
        geohash.encode(lat=45, lng=270),
        311
    )

    _tools.assert_equal(
        geohash.encode(lat=-87, lng=127),
        2595
    )

    _tools.assert_equal(
        geohash.encode(lat=17, lng=-42),
        4884
    )


def test_triangle_decode_icosahedron():
    geohash = _uut.Geohash(area_in_km_square=100 * 1000)

    index = 2510
    triangle = geohash.triangle(index=index, astype=_uut.AS_TYPE_TRIANGLE)
    _tools.assert_true(
        triangle.projected_on_sphere_contains(
            _point.Point.from_latlng(lat=-87, lng=127)
        )
    )

    _tools.assert_almost_equal(
        geohash.decode(index=index),
        triangle.center.to_unit()
    )

    index = 1689
    triangle = geohash.triangle(index=index, astype=_uut.AS_TYPE_TRIANGLE)
    _tools.assert_true(
        triangle.projected_on_sphere_contains(
            _point.Point.from_latlng(lat=17, lng=-42)
        )
    )

    _tools.assert_almost_equal(
        geohash.decode(index=index),
        triangle.center.to_unit()
    )


def test_triangle_decode_tetrahedron():
    geohash = _uut.Geohash(area_in_km_square=100 * 1000, sphere_approx=_uut.TETRAHEDRON)

    index = 2595
    triangle = geohash.triangle(index=index, astype=_uut.AS_TYPE_TRIANGLE)
    _tools.assert_true(
        triangle.projected_on_sphere_contains(
            _point.Point.from_latlng(lat=-87, lng=127)
        )
    )

    _tools.assert_almost_equal(
        geohash.decode(index=index),
        triangle.center.to_unit()
    )

    index = 4884
    triangle = geohash.triangle(index=index, astype=_uut.AS_TYPE_TRIANGLE)
    _tools.assert_true(
        triangle.projected_on_sphere_contains(
            _point.Point.from_latlng(lat=17, lng=-42)
        )
    )

    _tools.assert_almost_equal(
        geohash.decode(index=index),
        triangle.center.to_unit()
    )


def test_bbox():
    geohash = _uut.Geohash(area_in_km_square=100 * 1000)

    index = 2595
    triangle = geohash.triangle(index=index, astype=_uut.AS_TYPE_TRIANGLE)
    bbox = geohash.bbox(index=index)

    for point in triangle.points:
        _tools.assert_greater_equal(
            point.lat,
            bbox['s']
        )

        _tools.assert_less_equal(
            point.lat,
            bbox['n']
        )

        _tools.assert_greater_equal(
            point.lng,
            bbox['w']
        )

        _tools.assert_less_equal(
            point.lng,
            bbox['e']
        )
