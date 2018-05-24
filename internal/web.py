import cartwrap, gen2dict
import settings
from handlers import usa

import json
from flask import Flask, request, Response

app = Flask(__name__)

app.config['ENV'] = 'development' if settings.DEBUG else 'production'

cartogram_handlers = {
    'usa': usa.CartogramHandler()
}

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

