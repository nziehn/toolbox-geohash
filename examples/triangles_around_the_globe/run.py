import json

from toolbox import geohash as _geohash


def generate_html(google_maps_api_key, triangles):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Toolbox Geohash: Triangles around the globe</title>
    <style>
    html,
    body {
      height: 100%;
      margin: 0;
      padding: 0;
    }
    
    #map {
      height: 100%;
    }
    </style>
    </head>
    <body>
    <div id="map"></div>
    <!-- Replace the value of the key parameter with your own API key. -->
    <script async defer src="https://maps.googleapis.com/maps/api/js?key={google_maps_api_key}&callback=initMap">
    </script>
    
    <script>
    var infoWindow;
    var map;
    
    function initMap() {
      map = new google.maps.Map(document.getElementById('map'), {
        center: {
          lat: 0,
          lng: 0
        },
        zoom: 3
      });
      map.setMapTypeId(google.maps.MapTypeId.HYBRID);
    
      var triangles = {triangles};
      
      for (var triangle of triangles) {
        var polygon = new google.maps.Polygon({
          paths: triangle,
          strokeColor: '#0000FF',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#0000FF',
          fillOpacity: 0.2,
        });
        polygon.setMap(map);
      }
    }
    </script>
    
    </body>
    </html>
    '''.replace('{google_maps_api_key}', google_maps_api_key).replace('{triangles}', triangles)
    return html


def main(google_maps_api_key):
    geohash = _geohash.Geohash(area_in_km_square=1000 * 1000)
    triangles = []
    print(geohash.count_of_triangles())
    for index in range(geohash.count_of_triangles()):
        triangle = geohash.triangle(index=index)
        triangle.append(triangle[0])  # google requires the triangle to be closed
        triangles.append(triangle)

    html_code = generate_html(google_maps_api_key=google_maps_api_key, triangles=json.dumps(triangles))

    with open('example_triangles_around_the_globe.html', 'w') as outfile:
        outfile.write(html_code)


if __name__ == '__main__':
    main(google_maps_api_key='YOUR_GOOGLE_API_KEY_HERE')