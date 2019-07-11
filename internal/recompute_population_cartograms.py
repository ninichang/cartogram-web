import web
import json
import csv
import cartwrap, gen2dict, geojson_extrema
import settings
import os
import io

for sysname, handler in web.cartogram_handlers.items():

    with open("static/cartdata/{}/population.json".format(sysname)) as population_json_file:
        orig_population_json = json.load(population_json_file)

        tooltip = orig_population_json['tooltip']

    os.rename("static/cartdata/{}/population.json".format(sysname), "static/cartdata/{}/population.json.bak".format(sysname))

    pop_values = []

    with open("static/cartdata/{}/template.csv".format(sysname), newline='') as template_csv:
        
        template_reader = csv.DictReader(template_csv)

        for row in template_reader:

            pop_values.append(row['Population'])
    
    area_data = handler.gen_area_data(pop_values)

    cartogram_output = ""

    for source, line in cartwrap.generate_cartogram(area_data, handler.get_gen_file(), settings.CARTOGRAM_EXE):

        if source == "stderr":
            print("Generating {}: {}".format(sysname, line.decode()))
        else:
            cartogram_output += line.decode()
    
    if handler.expect_geojson_output():

        cartogram_json = json.loads(cartogram_output)

        if "bbox" not in cartogram_json:
                cartogram_json["bbox"] = geojson_extrema.get_extrema_from_geojson(cartogram_json)
    
    else:
        
        cartogram_json = gen2dict.translate(io.StringIO(cartogram_output), settings.CARTOGRAM_COLOR, handler.remove_holes())
    
    cartogram_json['tooltip'] = tooltip

    with open("static/cartdata/{}/population.json".format(sysname), 'w') as population_json_file:

        json.dump(cartogram_json, population_json_file)