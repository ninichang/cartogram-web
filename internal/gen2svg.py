import gen2dict
import sys

with open(sys.argv[1]) as map_gen_file:
    gen_json = gen2dict.translate(map_gen_file, "#aaaaaa", True)

with open(sys.argv[2], "w") as svg_file:

    max_x = gen_json["extrema"]["max_x"]
    min_x = gen_json["extrema"]["min_x"]
    max_y = gen_json["extrema"]["max_y"]
    min_y = gen_json["extrema"]["min_y"]

    width = max_x - min_x
    height = max_y - min_y


    scale = 750.0/width
    
    width *= scale
    height *= scale
    
    def x_transform(x):

        return (x - min_x)*scale
    
    def y_transform(y):

        return ((max_y-min_y) - (y - min_y))*scale
    
    svg_file.write("""<svg version="1.1"
baseProfile="full"
width="{}" height="{}"
xmlns="http://www.w3.org/2000/svg"
xmlns:gocart="https://go-cart.io">
""".format(round(width,2), round(height, 2)))

    for feature in gen_json["features"]:

        polygon_path = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), feature["coordinates"])))

        hole_paths = []

        for hole in feature['holes']:

            hole_points = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), hole)))
            hole_path = "M {} z".format(hole_points)
            hole_paths.append(hole_path)
        
        path = "M {} z {}".format(polygon_path, " ".join(hole_paths))

        #region = find_region_by_id(feature["properties"]["cartogram_id"])

        svg_file.write('<path d="{}" id="polygon-{}" class="region-{}" fill="#aaaaaa" stroke="#000000" stroke-width="1"/>\n'.format(path, feature["properties"]["polygon_id"], feature["properties"]["cartogram_id"]))
    
    svg_file.write("</svg>")
