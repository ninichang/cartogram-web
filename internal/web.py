import cartwrap, gen2dict
import settings
from handlers import usa, india, china

import json
import csv
import codecs
import re
import io
import string
import random
import datetime
from flask import Flask, request, Response, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "LTTNWg8luqfWKfDxjFaeC3vYoGrC2r2f5mtXo5IE/jt1GcY7/JaSq8V/tB"
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development' if settings.DEBUG else 'production'

db = SQLAlchemy(app)

cartogram_handlers = {
    'usa': usa.CartogramHandler(),
    'india': india.CartogramHandler(),
    'china': china.CartogramHandler()
}

default_cartogram_handler = "usa"

class CartogramEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string_key = db.Column(db.String(32), unique=True, nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)
    handler = db.Column(db.String(100), nullable=False)
    areas_string = db.Column(db.UnicodeText(), nullable=False)
    cartogram_data = db.Column(db.UnicodeText(), nullable=False)
    cartogramui_data = db.Column(db.UnicodeText(), nullable=False)

    def __repr__(self):
        return "<CartogramEntry {}>".format(self.string_key)

def get_random_string(length):

    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

@app.route('/', methods=['GET'])
def index():

    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('new_index.html', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=default_cartogram_handler)

@app.route('/cart/<string_key>', methods=['GET'])
def cartogram_by_key(string_key):

    cartogram_entry = CartogramEntry.query.filter_by(string_key=string_key).first_or_404()

    if cartogram_entry.handler not in cartogram_handlers:
        return Response('Error', status=500)
    
    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('new_cartogram.html', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=cartogram_entry.handler, cartogram_data=cartogram_entry.cartogram_data, cartogramui_data=cartogram_entry.cartogramui_data)
    


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
        json_response['tooltip'] = cart_data[2]       

        cartogram_entry_key = get_random_string(32)

        json_response['unique_sharing_key'] = cartogram_entry_key

        new_cartogram_entry = CartogramEntry(string_key=cartogram_entry_key, date_created=datetime.datetime.today(), handler=request.form['handler'], areas_string=cart_data[0], cartogram_data="{}", cartogramui_data=json.dumps(json_response))

        db.session.add(new_cartogram_entry)
        db.session.commit()

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
    
    handler = request.form['handler']
    cartogram_handler = cartogram_handlers[handler]

    if 'values' not in request.form:
        return Response('{"error":"badrequest"}', status=400, content_type="application/json")
    
    values = request.form['values'].split(";")

    try:
        values = [float(i) for i in values]
    except ValueError:
        return Response('{"error":"badvalues"}', status=400, content_type="application/json")
    
    if cartogram_handler.validate_values(values) != True:
        return Response('{"error":"badvalues"}', status=400, content_type="application/json")
    
    unique_sharing_key = ""

    if 'unique_sharing_key' in request.form:
        unique_sharing_key = request.form['unique_sharing_key']
    
    #cartogram_output = cartwrap.generate_cartogram(cartogram_handler.gen_area_data(values), cartogram_handler.get_gen_file(), "{}/cartogram".format(settings.CARTOGRAM_DATA_DIR))

    #return Response(json.dumps(gen2dict.translate(cartogram_output, settings.CARTOGRAM_COLOR)), status=200, content_type="application/json")

    def generate_streamed_json_response():

        cartogram_gen_output = b''
        current_loading_point = "null"

        yield '{"loading_progress_points":['

        for source, line in cartwrap.generate_cartogram(cartogram_handler.gen_area_data(values), cartogram_handler.get_gen_file(), "{}/cartogram".format(settings.CARTOGRAM_DATA_DIR)):

            if source == "stdout":
                cartogram_gen_output += line
            else:
                s = re.search(r'max\. abs\. area error: (.+)', line.decode())

                if s != None:
                    current_loading_point = s.groups(1)[0]
                
                yield '{{"loading_point": {}, "stderr_line": "{}"}},'.format(current_loading_point, line.decode())
        
        # We create a fake last entry because you can't have dangling commas in JSON
        yield '{"loading_point":0}],"cartogram_data":'

        cartogram_json = gen2dict.translate(io.StringIO(cartogram_gen_output.decode()), settings.CARTOGRAM_COLOR)        

        cartogram_json['unique_sharing_key'] = unique_sharing_key
        cartogram_json = json.dumps(cartogram_json)

        cartogram_entry = CartogramEntry.query.filter_by(string_key=unique_sharing_key).first()

        if cartogram_entry != None:
            cartogram_entry.cartogram_data = cartogram_json
            db.session.commit()

        yield cartogram_json

        yield "}"
    
    return Response(generate_streamed_json_response(), content_type='application/json', status=200)            

if __name__ == '__main__':
    app.run(debug=settings.DEBUG,host=settings.HOST,port=settings.PORT)

