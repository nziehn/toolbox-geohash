from toolbox.geohash.lib import tetrahedron as _uut

from nose import tools as _tools


def test_bounds_function():
    area_in_km_square = 1000 * 1000
    icosahedron = _uut.Tetrahedron.from_typical_area(area_in_km_square=area_in_km_square)

    min_area = None
    max_area = None
    total_area = 0

    for index in range(icosahedron.count_of_triangles):
        triangle = icosahedron.triangle_from_index(index=index)
        area = triangle.area_on_earth()

        min_area = area if min_area is None else min(min_area, area)
        max_area = area if max_area is None else max(max_area, area)
        total_area += area

    mean_area = total_area / icosahedron.count_of_triangles

    bounds = icosahedron.bounds_of_hashed_area()

    _tools.assert_almost_equal(
        min_area,
        bounds['min']
    )

    _tools.assert_almost_equal(
        max_area,
        bounds['max']
    )

    _tools.assert_almost_equal(
        mean_area,
        bounds['mean']
    )


def test_from_typical_area():
    # test for areas of 1m^2 to 100 km^2
    for exponent in range(11):
        area_in_km_square = 1e-06 * pow(10, exponent)
        icosahedron = _uut.Tetrahedron.from_typical_area(area_in_km_square=area_in_km_square)
        bounds = icosahedron.bounds_of_hashed_area()

        print(exponent, area_in_km_square / bounds['mean'], area_in_km_square)
        _tools.assert_less_equal(
            area_in_km_square / bounds['mean'],
            1.05
        )

        _tools.assert_greater_equal(
            area_in_km_square / bounds['mean'],
            1.00
        )