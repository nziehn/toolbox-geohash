# toolbox-geohash

This package provides a alternative to the typical geohashing libs - please note that the hashes produces by this library
are not compatible with the ones calculated from "typical" geohashing libraries. 

### What is the difference?

In contrast to the typical geohashing approach which is using rectangles to map areas on the map to a single index, 
toolbox-geohash is building the hashes from triangles.

### Why use this library over the typical approach?

There are three problems with the typical geohashing approach:

- In typical geohashing, the area on the map that is hashed to the same location vastly differs depending on the latitude of the coordinate that gets hashed. In this library (with default settings) the maximum size difference between maximum and minimum hashed area size is a factor of 2.
- In typical geohashing, the area on the map is not a square but (depending on selected precision) a skewed rectangle that is far from a square. In the this library you get triangles that are very close to equilateral triangles regardless of precision.
- In typical geohashing, you are very restricted in the selection of how big a hashed area should be. Typically, increasing the precision by 1 cuts the area in half which makes very big steps. In this library you can scale the area in very small steps to fit your usecase as close as possible.


## Features

- Encode geo coordinates (lat, lng) to geohashes (integer)
- Chose desired "precision" defined by the area of each hash value in km^2 - allows for (almost) arbitrary precision 
- Hashed area is always a triangle that is almost a perfect equilateral triangle
- Access center, triangle vertices or bounding box of the hashed area given the index
    

## Installation

Use your favourite python package installer, e.g.:
```
pip install toolbox-geohash
```


## Basic Usage

Create a geohasher and configure the desired precision by providing `area_in_km_squared`

```python
from toolbox import geohash as _geohash

geohash = _geohash.Geohash(area_in_km_square=1)
```

#### Encode coordinates

Encode a coordinate by providing latitude and longitude

```python
golden_gate_bridge_coordinates = dict(lat=37.8199011, lng=-122.4787358)
hash_index = geohash.encode(**golden_gate_bridge_coordinates)

# or directly...
hash_index = geohash.encode(lat=37.8199011, lng=-122.4787358)
```

#### Decode coordinates

Decode an index to latitude, longitude and get the center of the hashed triangle 
```python 
center = geohash.decode(index=hash_index)
print('The golden gate bridge is very close to: {lat}, {lng}'.format(lat=center.lat, lng=center.lng))
# The golden gate bridge is very close to: 37.820422796393814, -122.48007609149462
```

#### Access the entire hashed area, the triangle

You can get the vertices of the triangle that defines a single hash index by calling:
```python
triangle = geohash.triangle(index=hash_index)
# returns the triangle verteces of the hashed location
# [{'lat': 37.82226665048282, 'lng': -122.48068816364312}, {'lat': 37.81991667087469, 'lng': -122.4777825583044}, {'lat': 37.8190850320538, 'lng': -122.48175755307848}]
```

#### Accesing the bounding box

You can also access the bounding box of the triangle using:
```python
bounding_box = geohash.bbox(index=hash_index)
# access bounding_box.n for the norther bound of the bounding box (latitude)
# access bounding_box.s for the southern ... (latitude)
# access bounding_box.w for the western ... (longitude)
# access bounding_box.e for the eastern ... (longitude)
```

#### Actual size of the triangles

If you want to better understand the possible sizes of triangles for your specific choice of area_in_km_squared, 
you can approximate the triangle sizes (based on the assumption earth is a perfect sphere) using:

```python
triangle_sizes = geohash.bounds_of_hashed_area()
print(triangle_sizes)
# the sizes are in km^2: {'min': 0.6053713262068032, 'max': 1.206123527674693, 'mean': 0.9996324402788024}

# the mean triangle size is very close to what ever area_in_km_square you put in:
geohash_1km = _geohash.Geohash(area_in_km_square=1)
geohash_1_01km = _geohash.Geohash(area_in_km_square=1.01)
print(
    geohash_1km.bounds_of_hashed_area()['mean'],
    geohash_1_01km.bounds_of_hashed_area()['mean']
)
# 1 vs 0.9996324402788024 and 1.01 vs 1.009601785616878
```
