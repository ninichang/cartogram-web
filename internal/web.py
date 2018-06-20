import cartwrap, gen2dict
import settings
from handlers import usa, india, china

import json
import csv
import codecs
from flask import Flask, request, Response, flash, redirect, render_template, url_for

app = Flask(__name__)

app.secret_key = "LTTNWg8luqfWKfDxjFaeC3vYoGrC2r2f5mtXo5IE/jt1GcY7/JaSq8V/tB"

app.config['ENV'] = 'development' if settings.DEBUG else 'production'


cartogram_handlers = {
    'usa': usa.CartogramHandler(),
    'india': india.CartogramHandler(),
    'china': china.CartogramHandler()
}

default_cartogram_handler = "usa"

@app.route('/', methods=['GET'])
def index():

    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('new_index.html', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=default_cartogram_handler)

@app.route('/cartogramui', methods=['POST'])
def cartogram_ui():

    json_response = {}

    if 'handler' not in request.form:

        json_response['error'] = 'You must specify a handler.'
        return Response(json.dumps(json_response), status=200, content_type="application/json")
    
    if request.form['handler'] not in cartogram_handlers:

        json_response['error'] = 'The handler specified was invaild.'
        return Response(json.dumps(json_response), status=200, content_type="application/json")

    if 'csv' not in request.files:

        json_response['error'] = 'You must upload CSV data.'
        return Response(json.dumps(json_response), status=200, content_type="application/json")
    
    cartogram_handler = cartogram_handlers[request.form['handler']]

    try:

        # This is necessary because Werkzeug's file stream is in binary mode
        csv_codec = codecs.iterdecode(request.files['csv'].stream, 'utf-8')
        cart_data = cartogram_handler.csv_to_area_string_and_colors(csv_codec)

        json_response['error'] = "none"
        json_response['areas_string'] = cart_data[0]
        json_response['color_data'] = cart_data[1]

        return Response(json.dumps(json_response), status=200, content_type="application/json")

    except (KeyError, csv.Error, ValueError, UnicodeDecodeError) as error:

        json_response['error'] = 'There was a problem reading your CSV file.'
        return Response(json.dumps(json_response), status=200, content_type="application/json")

@app.route('/cartogram', methods=['POST'])
def cartogram():

    if 'handler' not in request.form:
        return Response('{"error":"badrequest"}', status=400, content_type="application/json")
    
    if request.form['handler'] not in cartogram_handlers:
        return Response('{"error":"badhandler"}', status=404, content_type="application/json")
    
    cartogram_handler = cartogram_handlers[request.form['handler']]

    if 'values' not in request.form:
        return Response('{"error":"badrequest"}', status=400, content_type="application/json")
    
    values = request.form['values'].split(";")

    try:
        values = [float(i) for i in values]
    except ValueError:
        return Response('{"error":"badvalues"}', status=400, content_type="application/json")
    
    if cartogram_handler.validate_values(values) != True:
        return Response('{"error":"badvalues"}', status=400, content_type="application/json")
    
    cartogram_output = cartwrap.generate_cartogram(cartogram_handler.gen_area_data(values), cartogram_handler.get_gen_file(), "{}/cartogram".format(settings.CARTOGRAM_DATA_DIR))

    return Response(json.dumps(gen2dict.translate(cartogram_output, settings.CARTOGRAM_COLOR)), status=200, content_type="application/json")

if __name__ == '__main__':
    app.run(debug=settings.DEBUG,host=settings.HOST,port=settings.PORT)

