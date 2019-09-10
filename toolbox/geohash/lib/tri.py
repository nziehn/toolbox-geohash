import math as _math
import numpy as _numpy
from toolbox.geohash.lib import util as _util


class Tri(object):
    def __init__(self, *points):
        if not points or len(points) != 3:
            raise ValueError('Must provide 3 points')

        self._points = tuple(points)

    @classmethod
    def from_rays(cls, *rays):
        if not rays or len(rays) != 2:
            raise ValueError('Must provide 2 rays!')

        face_set = {rays[0].start, rays[0].end}.union([rays[1].start, rays[1].end])
        if len(face_set) != 3:
            raise ValueError('Rays do not provide 3 vertices')

        return Tri(*sorted(face_set))

    @property
    def points(self):
        return self._points

    @property
    def source(self):
        return self.points[0]

    @property
    def vectors(self):
        return self.points[1] - self.source, self.points[2] - self.source

    def __hash__(self):
        return tuple(sorted(self._points)).__hash__()

    def __eq__(self, other):
        return tuple(sorted(self._points)) == tuple(sorted(other._points))

    def __repr__(self):
        return 'Triangle({}, {}, {})'.format(*self.points)

    @property
    def angle(self):
        a, b = self.vectors
        return _util.angle(a=a, b=b)

    @property
    def center(self):
        return (self._points[0] + self._points[1] + self._points[2]) / len(self._points)

    def project_on_unit_sphere(self):
        return Tri(*[p.to_unit() for p in self._points])

    def intersection_with_ray_from_origin(self, point):
        try:
            vectors = self.vectors
            a = _numpy.array(
                [
                    [vectors[0].x, vectors[1].x, -point.x],
                    [vectors[0].y, vectors[1].y, -point.y],
                    [vectors[0].z, vectors[1].z, -point.z],
                ]
            )
            b = _numpy.array(
                [
                    - self.source.x,
                    - self.source.y,
                    - self.source.z,
                ]
            )
            fraction_side1, fraction_side2, distance_center = _numpy.linalg.solve(a, b)
            return fraction_side1, fraction_side2, distance_center
        except ValueError as e:
            print(e)
            return None, None, None

    def projected_on_sphere_contains(self, point):
        fraction_side1, fraction_side2, distance_center = self.intersection_with_ray_from_origin(point)
        return (
            0 <= fraction_side1 < 1
            and 0 <= fraction_side2 < 1
            and 0 <= distance_center <= 1
        )

    def to_latlng_dict(self):
        return [{'lat': p.lat, 'lng': p.lng} for p in self._points]

    def area_on_sphere(self):
        angle_a = _util.angle(a=self._points[1], b=self._points[2])
        angle_b = _util.angle(a=self._points[2], b=self._points[0])
        angle_c = _util.angle(a=self._points[0], b=self._points[1])
        s = (angle_a + angle_b + angle_c) / 2

        spherical_excess = _math.atan(
            _math.sqrt(
                _math.tan(s / 2)
                * _math.tan((s - angle_a) / 2)
                * _math.tan((s - angle_b) / 2)
                * _math.tan((s - angle_c) / 2)
            )
        ) * 4

        return spherical_excess

    def area_on_earth(self):
        return self.area_on_sphere() * _util.EARTH_RADIUS ** 2
