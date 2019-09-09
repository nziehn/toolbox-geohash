import math as _math
from toolbox.geohash.lib import util as _util
from toolbox.geohash.lib import point as _point
from toolbox.geohash.lib import tri as _tri
from toolbox.geohash.lib import sphere_approx as _sphere_approx


class Tetrahedron(_sphere_approx.SphereApprox):
    _face_cnt = 4

    interior_angle = _util.deg2rad(60)
    root_north_latitude = _util.rad2deg(_math.asin(1 / 3.))
    south = _point.Point.from_latlng(-90, 0)
    north_center = _point.Point.from_latlng(root_north_latitude, 0)
    north_west = _point.Point.from_latlng(root_north_latitude, -120)
    north_east = _point.Point.from_latlng(root_north_latitude, 120)

    def __init__(self, divisions):
        super(Tetrahedron, self).__init__(divisions=divisions)

        self._vertices = [
            self.south,
            self.north_center,
            self.north_east,
            self.north_west,
        ]

        self._faces = [
            _tri.Tri(self.north_center, self.north_west, self.north_east),
            _tri.Tri(self.south, self.north_center, self.north_east),
            _tri.Tri(self.south, self.north_east, self.north_west),
            _tri.Tri(self.south, self.north_west, self.north_center),
        ]

        self._max_edge_length = (self._faces[0].center.to_unit() - self._faces[0].source).length
