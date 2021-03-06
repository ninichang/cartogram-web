import sys
import json

def mappackify(map_name):

    mappack = {}

    with open("static/cartdata/{}/abbreviations.json".format(map_name), "r") as abbreviations_json:

        mappack['abbreviations'] = json.load(abbreviations_json)

    with open("static/cartdata/{}/colors.json".format(map_name), "r") as colors_json:

        mappack['colors'] = json.load(colors_json)

    with open("static/cartdata/{}/config.json".format(map_name), "r") as config_json:

        mappack['config'] = json.load(config_json)

    with open("static/cartdata/{}/griddocument.json".format(map_name), "r") as griddocument_json:

        mappack['griddocument'] = json.load(griddocument_json)

    with open("static/cartdata/{}/labels.json".format(map_name), "r") as labels_json:

        mappack['labels'] = json.load(labels_json)

    with open("static/cartdata/{}/original.json".format(map_name), "r") as original_json:

        mappack['original'] = json.load(original_json)

    with open("static/cartdata/{}/population.json".format(map_name), "r") as population_json:

        mappack['population'] = json.load(population_json)
    
    with open("static/cartdata/{}/mappack.json".format(map_name), "w") as mappack_file:

        json.dump(mappack, mappack_file)

if __name__ == "__main__":

    mappackify(sys.argv[1])