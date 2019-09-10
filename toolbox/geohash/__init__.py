from toolbox.geohash.lib import icosahedron as _icosahedron
from toolbox.geohash.lib import tetrahedron as _tetrahedron
from toolbox.geohash.lib import point as _point

ICOSAHEDRON = 'icosahedron'
TETRAHEDRON = 'tetrahedron'

AS_TYPE_LAT_LNG_LIST = 'lat_lng_list'
AS_TYPE_POINT_LIST = 'point_list'
AS_TYPE_DICT_LIST = 'dict_list'
AS_TYPE_TRIANGLE = 'triangle'


class Geohash(object):
    def __init__(self, area_in_km_square=None, divisions=None, sphere_approx=ICOSAHEDRON):
        """
        Create a Geohash object to get fast access to geohashing / decoing. You have to provide either area_in_km_square or divisions!

        To get higher precision of geohashes, you can chose a small value for area_in_km_square (this is just an approximation) or increase the number of divisions.

        To get a well distributed geoindex use sphere_approx=ICOSAHEDRON to get fast as possible geohashes use sphere_approx=TETRAHEDRON

        :param area_in_km_square: the estimated area that gets mapped to a single geohash
        :param divisions: this is more of an internal variable - you would typically just set area_in_km_square and let the tool calculate this. This number defines how often each face of the sphere approximation is cut into smaller triangles.
        :param sphere_approx: chose between ICOSAHEDRON and TETRAHEDRON: ICOSAHEDRON gives better distributed results, TETRAHEDRON is faster
        """

        if sphere_approx == ICOSAHEDRON:
            cls = _icosahedron.Icosahedron
        elif sphere_approx == TETRAHEDRON:
            cls = _tetrahedron.Tetrahedron
        else:
            raise ValueError('provided sphere approx not found')

        if area_in_km_square:
            self._sphere_approx = cls.from_typical_area(area_in_km_square=area_in_km_square)
        else:
            if divisions is None:
                raise ValueError('must provide either visions or area_in_km_square')
            self._sphere_approx = cls(divisions=divisions)

    def encode(self, lat, lng):
        """
        Encodes a lat, lng coordinates into a geohash (integer)
        :param lat: latitude of the location you wish to hash
        :param lng: longitude of the location you wish to hash
        :return: the geohash index (int) that was computed
        """
        return self._sphere_approx.index_of_triangle(
            _point.Point.from_latlng(lat=lat, lng=lng)
        )

    def decode(self, index):
        """
        Given a geohash index returns the center of the hashed area
        :param index: The geohash to decode
        :return: The center point of triangle, you can access $.lat and $.lng to access the coordinates
        """
        triangle = self._sphere_approx.triangle_from_index(index=index)
        return triangle.center.to_unit()

    def triangle(self, index, astype=AS_TYPE_DICT_LIST):
        """
        Returns the coordinates of the triangle vertices defined by the geohash provided.

        You can alter the return format by providing the astype parameter.
        :param index: The geohash to decode
        :param astype: Chose between AS_TYPE_LAT_LNG_LIST: list of tuples (lat, lng), AS_TYPE_DICT_LIST: list of dictionaries {'lat': lat, 'lng': lng}, AS_TYPE_POINT_LIST: list of points (internal class)
        :return: list (type depends on astype param) but defaults to dictionaries {'lat': lat, 'lng': lng}
        """
        triangle = self._sphere_approx.triangle_from_index(index=index)

        if astype == AS_TYPE_LAT_LNG_LIST:
            return [(p.lat, p.lng) for p in triangle.points]

        if astype == AS_TYPE_POINT_LIST:
            return [p for p in triangle.points]

        if astype == AS_TYPE_DICT_LIST:
            return [{'lat': p.lat, 'lng': p.lng} for p in triangle.points]

        if astype == AS_TYPE_TRIANGLE:
            return triangle

        raise ValueError('Provided astype not found')

    def bbox(self, index):
        """
        Returns a bounding box around the triangle defined by the geohash
        :param index: The geohash to decode
        :return: {'n': norther_bound_latitude, 's': southern_bound_latitude, 'e': eastern_bound_longitude, 'w': western_bound_longitude}
        """
        triangle = self._sphere_approx.triangle_from_index(index=index)
        lat_list = [p.lat for p in triangle.points]
        lng_list = [p.lng for p in triangle.points]
        north = max(lat_list)
        south = min(lat_list)
        west = min(lng_list)
        east = max(lng_list)

        return {
            'n': north,
            's': south,
            'e': east,
            'w': west,
        }

    @property
    def count_of_triangles(self):
        """
        The total number of triangles (hash values) available for this configuration.
        """
        return self._sphere_approx.count_of_triangles

    def __len__(self):
        """
        The total number of triangles (hash values) available for this configuration.
        """
        return self.count_of_triangles

    def bounds_of_hashed_area(self):
        return self._sphere_approx.bounds_of_hashed_area()
