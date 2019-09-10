import math
from toolbox.geohash.lib import util as _util


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_latlng(self, lat, lng, in_radians=False):
        if in_radians:
            lat_rad = lat
            lng_rad = lng
        else:
            lat_rad = _util.deg2rad(lat)
            lng_rad = _util.deg2rad(lng)

        x = math.cos(lat_rad) * math.cos(lng_rad)
        y = math.cos(lat_rad) * math.sin(lng_rad)
        z = math.sin(lat_rad)
        return Point(x=x, y=y, z=z)

    def to_unit(self):
        return self / self.length

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other, self.z / other)

    def __abs__(self):
        return self.length

    def __repr__(self):
        return 'Point(lat={}, lng={})'.format(self.lat, self.lng)

    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x

        if self.y != other.y:
            return self.y < other.y

        if self.z != other.z:
            return self.z < other.z

        return False

    def __eq__(self, other):
        return (self - other).length == 0

    def __hash__(self):
        return hash(repr(self))

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    @property
    def length(self):
        return pow(self.dot(self), 0.5)

    @property
    def lat(self):
        return _util.rad2deg(math.asin(self.to_unit().z))

    @property
    def lng(self):
        on_sphere = self.to_unit()
        return _util.rad2deg(math.atan2(on_sphere.y, on_sphere.x))

    def __iter__(self):
        return [self.x, self.y, self.z]

    def distance_along_great_circle(self, other):
        """
        Haversine formula
        """
        lat_diff = _util.deg2rad(other.lat - self.lat)
        lng_diff = _util.deg2rad(other.lng - self.lng)
        a = (
            math.sin(lat_diff / 2) * math.sin(lat_diff / 2)
            + math.cos(_util.deg2rad(self.lat)) * math.cos(_util.deg2rad(other.lat))
            * math.sin(lng_diff / 2) * math.sin(lng_diff / 2)
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = _util.EARTH_RADIUS * c
        return d