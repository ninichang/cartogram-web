# This file contains code that translates from .gen graphics files to Python
# dictionary objects.

import random
import sys
import json

def polygon_area(coordinates):

    area_sum = 0.0

    for i in range(len(coordinates)):

        x1 = coordinates[i % len(coordinates)][0]
        y1 = coordinates[i % len(coordinates)][1]
        x2 = coordinates[(i+1) % len(coordinates)][0]
        y2 = coordinates[(i+1) % len(coordinates)][1]

        area_sum += (x1 * y2) - (y1 * x2)
    
    return area_sum / 2.0


# This function turns .gen output from the C code into JSON plottable by D3. It returns a Python dictionary that can be
# easily turned into json via json.dump or json.dumps. You may invoke this module as a script:
# 
# $ python gen2dict.py [input_gen_file] [output_json_file] [default_color]
#
# This function takes as input:
#
# in_fp:    A stream that contains the .gen file contents
# color:    A default color in case color information cannot be added later. This color should be a hex color code
#           (.e.g. "#aaaaaa") or a valid CSS color name (e.g. "red")
def translate(in_fp, color, remove_holes=False):

    result = {'type': 'FeatureCollection', 'features': [], 'extrema': {'max_x': None, 'min_x': None, 'min_y': None, 'max_y': None}}
    polygon_id = 1

    while True:

        id = in_fp.readline()

        if id[-1] == "\n":
            id = id[:-1]

        if id == "END":
            break
        
        id_parts = id.split()
        id = id_parts[0]
        
        # Each polygon receives a unique numerical ID, starting from 1.
        # This will be the same for each map.
        # This allows us to do animations when we switch between cartograms in the website.
        feature = {'type': 'Feature', 'id': id, 'properties': {
            'name': 'UNKNOWN',
            'color': color,
            'attribute': str(random.randint(1,100)),
            'polygon_id': polygon_id,
        }, 'coordinates': [], 'holes': []}

        polygon_id += 1

        while True:

            try:
                x, y = [float(i) for i in in_fp.readline().split()]

                if result['extrema']['max_x'] == None:
                    result['extrema']['max_x'] = x
                
                if result['extrema']['max_y'] == None:
                    result['extrema']['max_y'] = y
                
                if result['extrema']['min_x'] == None:
                    result['extrema']['min_x'] = x
                
                if result['extrema']['min_y'] == None:
                    result['extrema']['min_y'] = y
                
                if x > result['extrema']['max_x']:
                    result['extrema']['max_x'] = x
                
                if x < result['extrema']['min_x']:
                    result['extrema']['min_x'] = x
                
                if y > result['extrema']['max_y']:
                    result['extrema']['max_y'] = y
                
                if y < result['extrema']['min_y']:
                    result['extrema']['min_y'] = y

                feature['coordinates'].append([x,y])
            except ValueError:
                break #The region has been completed
        
        if remove_holes:
            if polygon_area(feature['coordinates']) > 0.0: # If the polygon is a hole, add it to the previous polygon as a hole
                result['features'][-1]['holes'].append(feature['coordinates'])
            else:
                result['features'].append(feature)
        else:        
            result['features'].append(feature)
    
    return result

if __name__ == "__main__":

    gen_info = None

    with open(sys.argv[1], 'r') as genfile:

        gen_info = translate(genfile, sys.argv[3], True)
    
    with open(sys.argv[2], 'w') as jsonfile:

        json.dump(gen_info, jsonfile)

        


