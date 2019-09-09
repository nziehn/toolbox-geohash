import math as _math
from toolbox.geohash.lib import point as _point
from toolbox.geohash.lib import ray as _ray
from toolbox.geohash.lib import tri as _tri
from toolbox.geohash.lib import sphere_approx as _sphere_approx


class Icosahedron(_sphere_approx.SphereApprox):
    _face_cnt = 20

    def __init__(self, divisions):
        super(Icosahedron, self).__init__(divisions=divisions)

        golden_ratio = (1 + _math.sqrt(5))/2
        self._vertices = [
            _point.Point(0, 1, golden_ratio),
            _point.Point(0, -1, golden_ratio),
            _point.Point(0, 1, -golden_ratio),
            _point.Point(0, -1, -golden_ratio),

            _point.Point(1, golden_ratio, 0),
            _point.Point(-1, golden_ratio, 0),
            _point.Point(1, -golden_ratio, 0),
            _point.Point(-1, -golden_ratio, 0),

            _point.Point(golden_ratio, 0, 1),
            _point.Point(golden_ratio, 0, -1),
            _point.Point(-golden_ratio, 0, 1),
            _point.Point(-golden_ratio, 0, -1),
        ]

        edges = []
        for idx1, v1 in enumerate(self._vertices):
            for idx2, v2 in enumerate(self._vertices):
                if idx1 >= idx2:
                    continue

                if (v1 - v2).length == 2.0:
                    edges.append(_ray.Ray(v1, v2))

        known_faces = set()
        self._faces = []
        self._max_edge_length = 0
        for idx1, e1 in enumerate(edges):
            for idx2, e2 in enumerate(edges):
                if idx1 >= idx2:
                    continue

                try:
                    triangle = _tri.Tri.from_rays(e1, e2)
                except:
                    continue

                if ((triangle.points[0] - triangle.points[1]).length != 2
                        or (triangle.points[0] - triangle.points[2]).length != 2
                        or (triangle.points[1] - triangle.points[2]).length != 2):
                    continue

                if triangle not in known_faces:
                    known_faces.add(triangle)
                    projected = triangle.project_on_unit_sphere()
                    self._faces.append(projected)
                    center = projected.center.to_unit()
                    for p in projected.points:
                        self._max_edge_length = max(self._max_edge_length, (p - center).length)

        self._vertices = tuple(v.to_unit() for v in self._vertices)
        self._faces = tuple(self._faces)
