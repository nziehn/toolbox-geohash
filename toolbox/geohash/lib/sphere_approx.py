import math as _math
from toolbox.geohash.lib import tri as _tri
from toolbox.geohash.lib import util as _util


class SphereApprox(object):
    _face_cnt = 0

    def __init__(self, divisions):
        self._divisions = _math.ceil(divisions)
        self._vertices = None
        self._faces = None
        self._max_edge_length = None

    @classmethod
    def from_typical_area(cls, area_in_km_square):
        earth_surface_approx = 4 * _math.pi * (_util.EARTH_RADIUS ** 2)
        total_triangle_count = earth_surface_approx / area_in_km_square
        triangle_count_per_face = total_triangle_count / cls._face_cnt
        triangle_cnt_along_side = _math.sqrt(triangle_count_per_face)
        return cls(divisions=triangle_cnt_along_side - 1)

    @property
    def divisions(self):
        return self._divisions

    @property
    def count_of_triangles(self):
        return self._count_of_triangles_per_face() * len(self._faces)

    def _count_of_triangles_per_face(self):
        return (self._divisions + 1) ** 2

    def _intersect_with_ray_from_origin_to_point(self, point):
        fraction_side1 = None
        fraction_side2 = None
        dist_center = None
        side_idx = None
        found = False

        point = point.to_unit()
        for side_idx, face in enumerate(self._faces):
            if (point - face.center.to_unit()).length > self._max_edge_length:
                continue

            try:
                fraction_side1, fraction_side2, dist_center = face.intersection_with_ray_from_origin(point=point)
            except:
                continue

            if (dist_center is not None
                    and 0 <= dist_center <= 1
                    and fraction_side1 >= -1e-14
                    and fraction_side2 >= -1e-14
                    and 0 <= fraction_side1 + fraction_side2 <= 1):
                found = True
                break

        if not found:
            raise ValueError('Did not find intersection')

        return side_idx, fraction_side1, fraction_side2

    def _index_of_triangle_given_fraction_of_sides(self, fraction_side1, fraction_side2, angle):
        triangle_cnt_along_side = self._divisions + 1
        row_index = int(fraction_side2 * triangle_cnt_along_side)
        y = _math.sin(angle) * fraction_side2
        height_of_cell = _math.sin(angle) / triangle_cnt_along_side
        y_in_cell = y - row_index * height_of_cell

        x = fraction_side1
        column_index = int(x * triangle_cnt_along_side)
        x_in_cell = x - column_index / triangle_cnt_along_side

        is_upside_down = y_in_cell > height_of_cell * (1 - x_in_cell * triangle_cnt_along_side)

        index = (
            column_index * 2 + is_upside_down
            + pow(triangle_cnt_along_side, 2) - pow(triangle_cnt_along_side - row_index, 2)
        )
        return index

    def index_of_triangle(self, point):
        side_idx, fraction_side1, fraction_side2 = self._intersect_with_ray_from_origin_to_point(point=point)
        face = self._faces[side_idx]
        index_in_side = self._index_of_triangle_given_fraction_of_sides(
            fraction_side1=fraction_side1, fraction_side2=fraction_side2,
            angle=face.angle
        )
        return int(self._count_of_triangles_per_face() * side_idx + index_in_side)

    def triangle_from_index(self, index):
        triangle_cnt_along_side = self._divisions + 1
        relative = index / self._count_of_triangles_per_face()
        side_idx = int(relative)
        index_in_side = index - side_idx * self._count_of_triangles_per_face()
        row_index = triangle_cnt_along_side - _math.floor(_math.sqrt(self._count_of_triangles_per_face() - index_in_side - 1)) - 1

        index_in_row = index_in_side - triangle_cnt_along_side ** 2 + (triangle_cnt_along_side - row_index) ** 2
        is_upside_down, column_index = _math.modf(index_in_row / 2)
        is_upside_down, column_index = bool(is_upside_down), int(column_index)

        fraction_side2 = row_index / triangle_cnt_along_side
        fraction_side1 = column_index / triangle_cnt_along_side

        if is_upside_down:
            corner_defs = [
                (fraction_side1, fraction_side2 + 1 / triangle_cnt_along_side),
                (fraction_side1 + 1 / triangle_cnt_along_side, fraction_side2 + 1 / triangle_cnt_along_side),
                (fraction_side1 + 1 / triangle_cnt_along_side, fraction_side2),
            ]
        else:
            corner_defs = [
                (fraction_side1, fraction_side2),
                (fraction_side1 + 1 / triangle_cnt_along_side, fraction_side2),
                (fraction_side1, fraction_side2 + 1 / triangle_cnt_along_side)
            ]

        face = self._faces[side_idx]

        vertices = []

        for fraction_side1, fraction_side2 in corner_defs:
            vertex = (face.vectors[0] * fraction_side1 + face.vectors[1] * fraction_side2 + face.source)
            on_sphere = vertex.to_unit()
            vertices.append(on_sphere)

        return _tri.Tri(*vertices)

    def bounds_of_hashed_area(self):
        point_on_biggest_triangle = self._faces[0].center
        index_of_biggest = self.index_of_triangle(point=point_on_biggest_triangle)
        biggest = self.triangle_from_index(index=index_of_biggest)
        biggest_area = biggest.area_on_earth()

        smallest = self.triangle_from_index(index=0)
        smallest_area = smallest.area_on_earth()

        earth_surface_approx = 4 * _math.pi * (_util.EARTH_RADIUS ** 2)
        mean_area = earth_surface_approx / self.count_of_triangles

        return {
            'min': smallest_area,
            'max': biggest_area,
            'mean': mean_area
        }
