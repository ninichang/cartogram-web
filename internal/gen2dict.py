# This file contains code that translates from .gen graphics files to Python
# dictionary objects.

import random

def translate(in_fp, color):

    result = {'type': 'FeatureCollection', 'features': []}

    while True:

        id = in_fp.readline()
        id = id[:-1]

        if id == "END":
            break
        
        feature = {'type': 'Feature', 'id': id, 'properties': {
            'name': 'UNKNOWN',
            'color': color,
            'attribute': str(random.randint(1,100))
        }, 'coordinates': []}

        while True:

            try:
                x, y = [str(i) for i in in_fp.readline().split()]

                feature['coordinates'].append([float(x),float(y)])
            except ValueError:
                break #The region has been completed
        
        result['features'].append(feature)
    
    return result
        


