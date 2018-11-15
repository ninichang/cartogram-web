import requests
import sys
import json

# This script allows you to generate cartograms non-interactively using the
# go-cart.io website logic. Run
#
# python remotegen.py [go-cart.io server location] [map-type] [save-location]
#
# and pass the CSV data for the cartogram you want to generate on stdin. This
# script will then make a request to the server specified in the first argument
# (usually https://go-cart.io - do not include a trailing slash). The results
# will be saved in save-location_cartogram.json and
# save-location_cartogramui.json

files = {'csv': sys.stdin}
cartogramui_variables = {'handler': sys.argv[2]}

request_base = sys.argv[1]

cartogramui_r = requests.post(request_base + "/cartogramui", cartogramui_variables, files=files)

if cartogramui_r.status_code != 200:
    print("Cartogram UI request failed: {}".format(cartogramui_r.text))
    sys.exit(1)

cartogramui = cartogramui_r.json()

if cartogramui['error'] != 'none':
    print("Cartogram UI request failed: {}".format(cartogramui['error']))
    sys.exit(1)

cartogram_variables = {
    'handler': sys.argv[2],
    'values': cartogramui['areas_string'],
    'unique_sharing_key': cartogramui['unique_sharing_key']
}

cartogram_r = requests.post(request_base + "/cartogram", cartogram_variables)

if cartogram_r.status_code != 200:
    print("Cartogram request failed: {}".format(cartogram_r.text))

cartogram = json.loads(cartogram_r.text.replace("\n", ""), strict=False)

with open(sys.argv[3] + "_cartogramui.json", 'w') as cartogramui_file:
    json.dump(cartogramui, cartogramui_file)

with open(sys.argv[3] + "_cartogram.json", 'w') as cartogram_file:
    json.dump(cartogram['cartogram_data'], cartogram_file)