from xml.dom import minidom
import json
import sys

# This script takes an SVG file containing a map with label information and
# outputs the label JSON information to stdout. Run this script with
#
# python svg2labels.py [svg-file] [scale-x] [scale-y]
#
# Note that this script only supports files which were originally created by
# the go-cart web interface. Labels created manually, from scratch with a
# program like Inkscape are not yet supported.

svg_map = minidom.parse(sys.argv[1])
labels = {"scale_x": float(sys.argv[2]), "scale_y": float(sys.argv[3]), "labels": [], "lines": []}

def get_class_list(class_attr):

    return class_attr.split(" ")

for text in svg_map.getElementsByTagName("text"):

    if "cartogram-label" not in get_class_list(text.getAttribute("class")):
        continue
    
    label = {'x': float(text.getAttribute("x")), 'y': float(text.getAttribute("y")), 'text': text.firstChild.data}

    labels['labels'].append(label)

for line in svg_map.getElementsByTagName("line"):
    
    if "cartogram-label" not in get_class_list(text.getAttribute("class")):
        continue
    
    line = {'x1': float(line.getAttribute("x1")), 'x2': float(line.getAttribute("x2")), 'y1': float(line.getAttribute("y1")), 'y2': float(line.getAttribute("y2"))}

    labels['lines'].append(line)

print(json.dumps(labels))
    






