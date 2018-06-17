# This file contains code that translates from .gen graphics files to Python
# dictionary objects.

import random
import sys
import json

def translate(in_fp, color):

    result = {'type': 'FeatureCollection', 'features': [], 'extrema': {'max_x': None, 'min_x': None, 'min_y': None, 'max_y': None}}

    while True:

        id = in_fp.readline()

        if id[-1] == "\n":
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
        
        result['features'].append(feature)
    
    return result

if __name__ == "__main__":

    gen_info = None

    with open(sys.argv[1], 'r') as genfile:

        gen_info = translate(genfile, sys.argv[3])
    
    with open(sys.argv[2], 'w') as jsonfile:

        json.dump(gen_info, jsonfile)

        


