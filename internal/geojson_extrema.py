
def get_extrema_from_geojson(geojson):

    min_x = None
    max_x = None
    min_y = None
    max_y = None

    for feature in geojson["features"]:

        if feature["geometry"]["type"] == "Polygon":

            for path in feature["geometry"]["coordinates"]:

                for coord in path:

                    if max_x == None or coord[0] > max_x:
                        max_x = coord[0]
                    
                    if min_x == None or coord[0] < min_x:
                        min_x = coord[0]
                    
                    if max_y == None or coord[1] > max_y:
                        max_y = coord[1]
                    
                    if min_y == None or coord[1] < min_y:
                        min_y = coord[1]
        
        elif feature["geometry"]["type"] == "MultiPolygon":

            for polygon in feature["geometry"]["coordinates"]:

                for path in polygon:
                    
                    for coord in path:

                        if max_x == None or coord[0] > max_x:
                            max_x = coord[0]
                        
                        if min_x == None or coord[0] < min_x:
                            min_x = coord[0]
                        
                        if max_y == None or coord[1] > max_y:
                            max_y = coord[1]
                        
                        if min_y == None or coord[1] < min_y:
                            min_y = coord[1]
        
        else:
            raise Exception("Unsupported feature type {}".format(feature["geometry"]["type"]))
    
    return [
        min_x,
        min_y,
        max_x,
        max_y
    ]