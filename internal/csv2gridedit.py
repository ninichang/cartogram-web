import csv
import json
import sys

def translate(csvfile):

    gridedit_document = {
        'width': 0,
        'height': 0,
        'contents': [],
        'edit_mask': []
    }

    csvreader = csv.reader(csvfile)

    for row in csvreader:
        gridedit_document['height'] += 1
        gridedit_document['width'] = 0
        for col in row:
            gridedit_document['width'] += 1
            gridedit_document['contents'].append(col)

    return gridedit_document

if __name__ == "__main__":

    with open(sys.argv[1], newline='') as csvfile:

        gd = translate(csvfile)

        print(json.dumps(gd))

