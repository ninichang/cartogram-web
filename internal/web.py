import cartwrap, gen2dict
import settings
from handlers import usa

import json
import csv
import codecs
from flask import Flask, request, Response, flash, redirect, render_template, url_for

app = Flask(__name__)

app.secret_key = "LTTNWg8luqfWKfDxjFaeC3vYoGrC2r2f5mtXo5IE/jt1GcY7/JaSq8V/tB"

app.config['ENV'] = 'development' if settings.DEBUG else 'production'


cartogram_handlers = {
    'usa': usa.CartogramHandler()
}

@app.route('/', methods=['GET'])
def index():

    return render_template('new_index.html')

@app.route('/cartogramui', methods=['POST'])
def cartogram_ui():

    if 'handler' not in request.form:

        flash('You must specify a handler.')
        return redirect(url_for('index'))
    
    if request.form['handler'] not in cartogram_handlers:

        flash('The handler specified was invalid.')
        return redirect(url_for('index'))

    if 'csv' not in request.files:

        flash('You must upload CSV data.')
        return redirect(url_for('index'))
    
    cartogram_handler = cartogram_handlers[request.form['handler']]

    try:

        # This is necessary because Werkzeug's file stream is in binary mode
        csv_codec = codecs.iterdecode(request.files['csv'].stream, 'utf-8')
        cart_data = cartogram_handler.csv_to_area_string_and_colors(csv_codec)

        return render_template('cartogramui_new.html', area_string=cart_data[0], color_data=cart_data[1], cartogram_url=url_for('cartogram'), cartogram_data_dir=url_for('static', filename='cartdata'))

    except (KeyError, csv.Error, ValueError, UnicodeDecodeError) as error:

        flash('There was a problem reading your CSV file.')
        return redirect(url_for('index'))

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

