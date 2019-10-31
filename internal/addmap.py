import sys
import os
import io
import csv
import json
import shutil
import gen2dict
import svg2color
import svg2labels
import svg2config
import geojson_extrema
import traceback
import importlib
import cartwrap
import mappackify

def print_welcome():

    print("Welcome to the Add Map Wizard!")
    print()

def print_usage():

    print("Usage: ")
    print()
    print("init [map-name]\t\tStart the process of adding a new map")
    print("data [map-name]\t\tAdd dataset data, colors, and labels to a new map")

def init(map_name):

    def cleanup():

        print()
        print("I cannot continue. If you contact the developers for support, send the stacktrace below: ")
        print()
        traceback.print_stack(file=sys.stdout)

        print()
        print("An error occurred. Cleaning up...")

        try:
            os.remove("handlers/{}.py".format(map_name))
            os.remove("{}.svg".format(map_name))
        except OSError:
            pass
        
        shutil.rmtree("static/cartdata/{}".format(map_name), ignore_errors=True)

    if os.path.exists("handlers/{}.py".format(map_name)):
        print("Error: It looks like a map with the name '{}' already exists (I found handlers/{}.py).".format(map_name, map_name))
        return
    
    if os.path.exists("static/cartdata/{}".format(map_name)):
        print("Error: It looks like a map with the name '{}' already exists (I found static/cartdata/{}).".format(map_name, map_name))
        return
    
    user_friendly_name = input("Enter a user friendly name for this map: ")

    print()
    print("Now I need to know where the .json and .csv files for this map are located. These files should be located in the CARTOGRAM_DATA_DIR directory. You should supply me with a path relative to CARTOGRAM_DATA_DIR.")
    print("E.G: The .json file for this map is located at CARTOGRAM_DATA_DIR/map.json. Enter \"map.json\".")
    print()

    map_gen_path = input("Enter the location of the .json file for this map: ")
    map_dat_path = input("Enter the location of the .csv file for this map: ")

    if not os.path.exists("{}/{}".format(os.environ["CARTOGRAM_DATA_DIR"], map_gen_path)):
        print("Error: It looks like the file {}/{} does not exist.".format(os.environ["CARTOGRAM_DATA_DIR"], map_gen_path))
        return
    
    if not os.path.exists("{}/{}".format(os.environ["CARTOGRAM_DATA_DIR"], map_dat_path)):
        print("Error: It looks like the file {}/{} does not exist.".format(os.environ["CARTOGRAM_DATA_DIR"], map_dat_path))
        return
    
    with open("{}/{}".format(os.environ["CARTOGRAM_DATA_DIR"], map_dat_path), "r") as dat_file:
        dat_contents = dat_file.read()
    
    regions = []
    
    with open("{}/{}".format(os.environ["CARTOGRAM_DATA_DIR"], map_dat_path), newline='') as dat_file:

        reader = csv.DictReader(dat_file)

        for row in reader:

            regions.append({
                "id": row["Region Id"],
                "data": row["Region Data"],
                "name": row["Region Name"],
                "abbreviation": row["Region Abbreviation"]
            })
    
    def find_region_by_id(i):
        for region in regions:
            if region["id"] == i:
                return region
        
        return None
    
    region_identifier = input("What are the regions of this map called (e.g. State, Province)? ")
    dataset_name = input("What is the name of the dataset in the .dat file (e.g. GDP)? ")

    handler_py_template = '''import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "{0}"

    def get_gen_file(self):
        return "{{}}/{1}".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != {2}:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """{3}""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "{4}", 0, 1, 2, 3, [{5}], [0.0 for i in range(0,{2})], {{{6}}})
'''
    
    area_data_template = "\n".join(list(map(lambda region: "{} {{}} {}".format(region["id"], region["name"]), regions)))
    region_names = ",".join(list(map(lambda region: '"{}"'.format(region["name"]), regions)))
    region_name_id_dict = ",".join(list(map(lambda region: '"{}":"{}"'.format(region["name"], region["id"]), regions)))

    handler_py = handler_py_template.format(user_friendly_name, map_gen_path, len(regions), area_data_template, region_identifier, region_names, region_name_id_dict)

    print("Writing handlers/{}.py...".format(map_name))

    try:
        with open("handlers/{}.py".format(map_name), "w") as handler_file:

            try:
                handler_file.write(handler_py)
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    try:
        os.mkdir("static/cartdata/{}".format(map_name))
    except:
        cleanup()
        return
    
    print("Writing static/cartdata/{}/config.json...".format(map_name))

    try:
        with open("static/cartdata/{}/config.json".format(map_name), "w") as config_json_file:

            try:
                config_json_file.write("""{
    "dont_draw": [],
    "elevate": []
}""")
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    print("Writing static/cartdata/{}/abbreviations.json...".format(map_name))

    try:
        with open("static/cartdata/{}/abbreviations.json".format(map_name), "w") as abbreviations_json_file:

            try:
                abbreviations_json_file.write("{\n")
                abbreviations_json_file.write(",\n".join(list(map(lambda region: '"{}":"{}"'.format(region["name"], region["abbreviation"]), regions))))
                abbreviations_json_file.write("\n}")
            except:
                cleanup()
                return
    except:
        cleanup()
        return

    print("Writing static/cartdata/{}/colors.json...".format(map_name))

    try:
        with open("static/cartdata/{}/colors.json".format(map_name), "w") as colors_json_file:

            try:
                colors_json_file.write("{\n")
                colors_json_file.write(",\n".join(list(map(lambda region: '"id_{}":"#aaaaaa"'.format(region["id"]), regions))))
                colors_json_file.write("\n}")
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    print("Writing static/cartdata/{}/template.csv...".format(map_name))

    try:
        with open("static/cartdata/{}/template.csv".format(map_name), "w") as template_csv_file:

            try:
                template_csv_file.write('"{}","Population","{}","Colour"\n'.format(region_identifier, dataset_name))
                template_csv_file.write("\n".join(list(map(lambda region: '"{}","","{}",""'.format(region["name"], region["data"]), regions))))
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    print()
    print("I will now create {}.svg. You should edit this file to specify the default color and add labels for each region.".format(map_name))
    print("DO NOT RESIZE OR RESCALE THE CONTENTS OF THIS FILE! Accurate label placement depends on the scale calculated by this wizard.")
    print()

    try:
        with open("{}/{}".format(os.environ["CARTOGRAM_DATA_DIR"], map_gen_path), "r") as map_gen_file:

            geo_json = json.load(map_gen_file)

    except Exception as e:
        print(repr(e))
        cleanup()
        return

    print("Writing {}.svg...".format(map_name))

    try:
        with open("{}.svg".format(map_name), "w") as svg_file:

            try:

                max_x = geo_json["bbox"][2]
                min_x = geo_json["bbox"][0]
                max_y = geo_json["bbox"][3]
                min_y = geo_json["bbox"][1]

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

                next_polygon_id = 1

                for feature in geo_json["features"]:

                    if feature["geometry"]["type"] == "Polygon":

                        polygon_path = None
                        hole_paths = []
                        polygon_id = next_polygon_id

                        for path in feature["geometry"]["coordinates"]:

                            next_polygon_id += 1

                            if polygon_path == None:

                                polygon_path = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), path)))
                                
                            else:

                                hole_path = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), path)))

                                hole_paths.append("M {} z".format(hole_path))
                        
                        path = "M {} z {}".format(polygon_path, " ".join(hole_paths))

                        region = find_region_by_id(feature["properties"]["cartogram_id"])

                        svg_file.write('<path gocart:regionname="{}" d="{}" id="polygon-{}" class="region-{}" fill="#aaaaaa" stroke="#000000" stroke-width="1"/>\n'.format(region["name"], path, polygon_id, feature["properties"]["cartogram_id"]))
                    elif feature["geometry"]["type"] == "MultiPolygon":

                        for polygon in feature["geometry"]["coordinates"]:

                            polygon_path = None
                            hole_paths = []
                            polygon_id = next_polygon_id

                            for path in polygon:

                                next_polygon_id += 1

                                if polygon_path == None:

                                    polygon_path = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), path)))
                                    
                                else:

                                    hole_path = " ".join(list(map(lambda coord: "{} {}".format(round(x_transform(coord[0]), 3), round(y_transform(coord[1]), 3)), path)))

                                    hole_paths.append("M {} z".format(hole_path))
                            
                            path = "M {} z {}".format(polygon_path, " ".join(hole_paths))

                            print(feature["properties"]["cartogram_id"])

                            region = find_region_by_id(feature["properties"]["cartogram_id"])

                            print(repr(region))

                            svg_file.write('<path gocart:regionname="{}" d="{}" id="polygon-{}" class="region-{}" fill="#aaaaaa" stroke="#000000" stroke-width="1"/>\n'.format(region["name"], path, polygon_id, feature["properties"]["cartogram_id"]))
                    else:
                        raise Exception("Unsupported feature type {}.".format(feature["geometry"]["type"]))
                
                svg_file.write("</svg>")
            
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return

    print("Writing static/cartdata/{}/labels.json...".format(map_name))

    try:
        with open("static/cartdata/{}/labels.json".format(map_name), "w") as labels_json_file:

            try:
                labels_json_file.write('{{"scale_x": {0}, "scale_y": {0}, "labels": [], "lines": []}}'.format(scale))
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now create {0}-landarea.csv and {0}-population.csv. You should edit these files to specify the land area (in square kilometers) and population of each region.".format(map_name))
    print("DO NOT ALTER THE COLOR INFORMATION IN THESE FILES! You should specify the color for each region by editing {}.svg".format(map_name))
    print()

    print("Writing {}-landarea.csv...".format(map_name))

    try:
        with open("{}-landarea.csv".format(map_name), "w") as template_csv_file:

            try:
                template_csv_file.write('"{}","","Land Area","Colour"\n'.format(region_identifier))
                template_csv_file.write("\n".join(list(map(lambda region: '"{}","","","#aaaaaa"'.format(region["name"]), regions))))
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    print("Writing {}-population.csv...".format(map_name))

    try:
        with open("{}-population.csv".format(map_name), "w") as template_csv_file:

            try:
                template_csv_file.write('"{}","","Population","Colour"\n'.format(region_identifier))
                template_csv_file.write("\n".join(list(map(lambda region: '"{}","","","#aaaaaa"'.format(region["name"]), regions))))
            except:
                cleanup()
                return
    except:
        cleanup()
        return
    
    print()
    print("I will now modify web.py to add your new map. Before I do this, I will back up the current version of web.py to web.py.bak.")
    print()

    print("Backing up web.py...")

    try:
        shutil.copy("web.py", "web.py.bak")
    except:
        cleanup()
        return

    print("Editing web.py...")

    try:
        with open("web.py", "r") as web_py_file:

            try:
                web_py_contents = web_py_file.read()
                web_py_lines = web_py_contents.split("\n")
            except:
                cleanup()
                return
        
        web_py_new_lines = []
        found_header = False
        found_body = False
        for line in web_py_lines:

            if line.strip() == "# ---addmap.py header marker---":

                web_py_new_lines.append("from handlers import {}".format(map_name))
                web_py_new_lines.append("# ---addmap.py header marker---")
                found_header = True
            elif line.strip() == "# ---addmap.py body marker---":

                web_py_new_lines.append("'{0}': {0}.CartogramHandler(),".format(map_name))
                web_py_new_lines.append("# ---addmap.py body marker---")
                found_body = True
            else:
                web_py_new_lines.append(line)
        
        if not found_header or not found_body:
            print("I was not able to find the appropriate markers that allow me to modify the web.py file.")
            cleanup()
            return
        
        with open("web.py", "w") as web_py_file:

            try:
                web_py_file.write("\n".join(web_py_new_lines))
            except:
                print("An error occured while trying to write changes to web.py.")
                cleanup()
                return
    except:
        cleanup()
        return
        
    
    print()
    print("All done!")
    print()

def data(map_name):

    def cleanup():

        print()
        print("I cannot continue. If you contact the developers for support, send the stacktrace below: ")
        print()
        traceback.print_stack(file=sys.stdout)

        print()
        print("An error occurred. Cleaning up...")

        try:
            os.remove("static/cartdata/{}/population.json".format(map_name))
            os.remove("static/cartdata/{}/griddocument.json".format(map_name))
            os.remove("static/cartdata/{}/original.json".format(map_name))
        except OSError:
            pass

    if not os.path.exists("handlers/{}.py".format(map_name)):
        print("Error: It looks like a map with the name '{}' doesn't exist (I didn't find handlers/{}.py).".format(map_name, map_name))
        return
    
    if not os.path.exists("static/cartdata/{}".format(map_name)):
        print("Error: It looks like a map with the name '{}' doesn't exist (I didn't find static/cartdata/{}).".format(map_name, map_name))
        return
    
    if not os.path.exists("{}.svg".format(map_name)):
        print("Error: It looks like {}.svg doesn't exist. I need this file to add color information to your new map.")
        return
    
    if not os.path.exists("{}-landarea.csv".format(map_name)):
        print("Error: It looks like {}.svg doesn't exist. I need this file to add land area information to your new map.")
        return
    
    if not os.path.exists("{}-population.csv".format(map_name)):
        print("Error: It looks like {}.svg doesn't exist. I need this file to add population information to your new map.")
        return
    
    print()
    print("I will now parse {}.svg to learn each map region's default color.".format(map_name))
    print()

    print("Reading {}.svg...".format(map_name))

    try:
        new_colors, colors_by_name = svg2color.convert("{}.svg".format(map_name), "static/cartdata/{}/colors.json".format(map_name))
        print(repr(new_colors))
        print(repr(colors_by_name))
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now parse {}.svg for label information.".format(map_name))
    print()

    print("Reading static/cartdata/{}/labels.json...".format(map_name))
    try:
        with open("static/cartdata/{}/labels.json".format(map_name), "r") as labels_json_file:

            try:
                labels_json = json.load(labels_json_file)
                labels_scale_x = labels_json['scale_x']
                labels_scale_y = labels_json['scale_y']
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Reading {}.svg...".format(map_name))

    try:
        labels = svg2labels.convert("{}.svg".format(map_name), labels_scale_x, labels_scale_y)
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now parse {}.svg for configuration information.".format(map_name))
    print()
    
    print("Reading {}.svg...".format(map_name))

    try:
        config = svg2config.convert("{}.svg".format(map_name))
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now parse the land area and population information from each region from {0}-landarea.csv and {0}-population.csv".format(map_name))
    print()

    try:
        map_module = importlib.import_module('handlers.{}'.format(map_name))

        map_handler = map_module.CartogramHandler()

        print("Reading {}-landarea.csv...".format(map_name))
        with open("{}-landarea.csv".format(map_name), "r", newline='') as landarea_csv:

            try:
                landarea_cartogramui = map_handler.csv_to_area_string_and_colors(landarea_csv)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
        
        print("Reading {}-population.csv...".format(map_name))

        with open("{}-population.csv".format(map_name), "r", newline='') as population_csv:

            try:
                population_cartogramui = map_handler.csv_to_area_string_and_colors(population_csv)
                population_cartogramui[2]["unit"] = "people"
            except Exception as e:
                print(repr(e))
                cleanup()
                return
        
        print("Reading {}-population.csv...".format(map_name))
        regions_populations = {}
        with open("{}-population.csv".format(map_name), "r", newline='') as population_csv:

            try:
                reader = csv.reader(population_csv)

                header_row = True
                for row in reader:

                    if header_row:
                        header_row = False
                        continue
                    
                    regions_populations[row[0]] = row[2]
            except Exception as e:
                print(repr(e))
                cleanup()
                return
                    
    except Exception as e:
        print(repr(e))
        cleanup()
        return

    print()
    print("I will now generate the conventional and population map data. This may take a moment.")
    print()

    print("Generating population map...")
    try:

        areas = population_cartogramui[0].split(";")
        #areas = list(map(lambda area: float(area), areas))

        gen_output_lines = []

        for source, line in cartwrap.generate_cartogram(map_handler.gen_area_data(areas), map_handler.get_gen_file(), os.environ["CARTOGRAM_EXE"]):

            if source == "stdout":
                gen_output_lines.append(line.decode().strip())
            else:
                print("Generating population map: {}".format(line.decode().strip()))
        
        gen_output = "\n".join(gen_output_lines)

        with open("{}-population.gen".format(map_name), "w") as population_gen_file:
            population_gen_file.write(gen_output)

        cartogram_json = json.loads(gen_output)

        # Calculate the bounding box if necessary
        if "bbox" not in cartogram_json:
            cartogram_json["bbox"] = geojson_extrema.get_extrema_from_geojson(cartogram_json)

        cartogram_json["tooltip"] = population_cartogramui[2]
    except Exception as e:
        traceback.print_exc()
        print(repr(e))
        cleanup()
        return
    
    print()
    print("Generating conventional map...")
    try:

        with open(map_handler.get_gen_file(), "r") as map_gen_file:

            try:
                original_json = json.load(map_gen_file)

                original_tooltip = landarea_cartogramui[2]
                original_tooltip['unit'] = 'km sq.'

                original_json['tooltip'] = original_tooltip
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now generate the finalized data entry template.")
    print()

    print("Reading static/cartdata/{}/template.csv...".format(map_name))
    final_template = []
    try:

        with open("static/cartdata/{}/template.csv".format(map_name), "r", newline='') as template_csv_file:

            try:
                reader = csv.reader(template_csv_file)

                header_row = True
                for row in reader:

                    if header_row:
                        final_template.append(row)
                        header_row = False
                        continue
                    
                    final_template.append([row[0], regions_populations[row[0]], row[2], colors_by_name[row[0]]])
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/template.csv...".format(map_name))
    try:
        with open("static/cartdata/{}/template.csv".format(map_name), "w", newline='') as template_csv_file:

            try:
                writer = csv.writer(template_csv_file)

                for row in final_template:
                    writer.writerow(row)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Reading static/cartdata/{}/template.csv...".format(map_name))
    try:
        with open("static/cartdata/{}/template.csv".format(map_name), "r", newline='') as template_csv_file:

            try:
                cartogramui = map_handler.csv_to_area_string_and_colors(template_csv_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/griddocument.json...".format(map_name))
    try:
        with open("static/cartdata/{}/griddocument.json".format(map_name), "w") as griddocument_json_file:

            try:
                json.dump(cartogramui[3], griddocument_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("I will now finish up writing the map data files.")
    print()

    print("Writing static/cartdata/{}/original.json...".format(map_name))
    try:
        with open("static/cartdata/{}/original.json".format(map_name), "w") as original_json_file:

            try:
                json.dump(original_json, original_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/population.json...".format(map_name))
    try:
        with open("static/cartdata/{}/population.json".format(map_name), "w") as original_json_file:

            try:
                json.dump(cartogram_json, original_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/labels.json...".format(map_name))
    try:
        with open("static/cartdata/{}/labels.json".format(map_name), "w") as labels_json_file:

            try:
                json.dump(labels, labels_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/colors.json...".format(map_name))
    try:
        with open("static/cartdata/{}/colors.json".format(map_name), "w") as colors_json_file:

            try:
                json.dump(new_colors, colors_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Writing static/cartdata/{}/config.json...".format(map_name))
    try:
        with open("static/cartdata/{}/config.json".format(map_name), "w") as colors_json_file:

            try:
                json.dump(config, colors_json_file)
            except Exception as e:
                print(repr(e))
                cleanup()
                return
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print("Generating map pack in static/cartdata/{}/mappack.json...".format(map_name))

    try:
        mappackify.mappackify(map_name)
    except Exception as e:
        print(repr(e))
        cleanup()
        return
    
    print()
    print("All done!")
    print()

print_welcome()

if len(sys.argv) < 3:
    print_usage()
    sys.exit(1)

if sys.argv[1] == "init":
    init(sys.argv[2])
elif sys.argv[1] == "data":
    data(sys.argv[2])
else:
    print_usage()
    sys.exit(1)
