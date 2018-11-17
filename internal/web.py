import cartwrap, gen2dict
import settings
from handlers import usa, india, china, germany, brazil, brazil_combined, india_no_tg

import json
import csv
import codecs
import re
import io
import string
import random
import base64
import datetime
from flask import Flask, request, session, Response, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import validate_email
import smtplib
import email.mime.text
import socket

app = Flask(__name__)

app.secret_key = "LTTNWg8luqfWKfDxjFaeC3vYoGrC2r2f5mtXo5IE/jt1GcY7/JaSq8V/tB"
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
# This gets rid of an annoying Flask error message. We don't need this feature anyway.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development' if settings.DEBUG else 'production'

# Whenever you make changes to the DB models, you must generate the tables using db.create_all() as follows:
#
# $ source ./setupenv.sh
# (venv) $ python3
# (venv) >>> import web
# (venv) >>> web.db.create_all()
#
# NOTE: SQLAlchemy does not do database migrations. If you do change something, you'll need to figure out how to migrate
#       the data manually, or delete everything and start from scratch.
db = SQLAlchemy(app)

cartogram_handlers = {
    'usa': usa.CartogramHandler(),
    'india': india.CartogramHandler(),
    'india-no-tg': india_no_tg.CartogramHandler(),
    'china': china.CartogramHandler(),
    'germany': germany.CartogramHandler(),
    'brazil': brazil.CartogramHandler(),
    'brazil-combined': brazil_combined.CartogramHandler()    
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

# This function returns a random string containg lowercase letters and numbers that is *length* characters long.
# This is used to generate the unique string key associated with each cartogram.
def get_random_string(length):

    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))

@app.route('/', methods=['GET'])
def index():

    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('new_index.html', page_active='home', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=default_cartogram_handler)

@app.route('/faq', methods=['GET'])
def faq():

    return render_template('faq.html', page_active='faq')

@app.route('/anim/<animation_name>', methods=['GET'])
def anim(animation_name):

    next_url = request.args.get('next', '')
    display_next = len(next_url.strip()) > 0

    previous_url = request.args.get('prev', '')
    display_previous = len(previous_url.strip()) > 0

    question_no = request.args.get('hrq', '')
    display_question_no = len(question_no.strip()) > 0

    deactivate_list = request.args.get('deactivate', '')

    return render_template('anim.html', page_active='anim', animation_name=animation_name, display_next=display_next,next_url=next_url, display_question_no=display_question_no, question_no=question_no, deactivate_list=deactivate_list, previous_url=previous_url, display_previous=display_previous)

@app.route('/3maps', methods=['GET'])
def threemaps():

    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    next_url = request.args.get('next', '')
    display_next = len(next_url.strip()) > 0

    previous_url = request.args.get('prev', '')
    display_previous = len(previous_url.strip()) > 0

    question_no = request.args.get('hrq', '')
    display_question_no = len(question_no.strip()) > 0

    deactivate_list = request.args.get('deactivate', '')

    handler = request.args.get('handler', '')

    maps = request.args.get('maps', '')
    maps = base64.b64decode(maps).decode("utf-8")

    hide = request.args.get('hide', '')

    return render_template('3maps.html', page_active='3maps', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=default_cartogram_handler, display_next=display_next,next_url=next_url, display_question_no=display_question_no, question_no=question_no, deactivate_list=deactivate_list, maps=maps, handler=handler, previous_url=previous_url, display_previous=display_previous, hide=hide)

@app.route('/survey/<survey_name>', defaults={'survey_question': '0'})
@app.route('/survey/<survey_name>/<survey_question>', methods=['GET'])
def survey(survey_name, survey_question):

    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('survey.html', page_active='survey', cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=default_cartogram_handler, survey_name=survey_name,survey_question=int(survey_question))

@app.route('/tutorial', methods=['GET'])
def tutorial():

    return render_template('tutorial.html', page_active='tutorial')


@app.route('/gridedit', methods=['GET'])
def gridedit():

    return render_template('gridedit.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'GET':
        csrf_token = get_random_string(50)
        session['csrf_token'] = csrf_token

        return render_template('contact.html', page_active='contact',name="",message="",email_address="",subject="", csrf_token=csrf_token)
    else:
        
        name = request.form.get('name', '')
        email_address = request.form.get('email', '')
        subject = request.form.get('subject', '')
        message = request.form.get('message', '')
        csrf = request.form.get('csrftoken', '')

        if 'csrf_token' not in session:
            flash('Invalid CSRF token.', 'danger')
            csrf_token = get_random_string(50)
            session['csrf_token'] = csrf_token
            return render_template('contact.html', page_active='contact',name=name,message=message,email_address=email_address,subject=subject, csrf_token=csrf_token)
        
        if session['csrf_token'] != csrf or len(session['csrf_token'].strip()) < 1:
            flash('Invalid CSRF token.', 'danger')
            csrf_token = get_random_string(50)
            session['csrf_token'] = csrf_token
            return render_template('contact.html', page_active='contact',name=name,message=message,email_address=email_address,subject=subject, csrf_token=csrf_token)
        
        csrf_token = get_random_string(50)
        session['csrf_token'] = csrf_token

        if len(name.strip()) < 1 or len(subject.strip()) < 1 or len(message.strip()) < 1:
            flash('You must fill out all of the form fields', 'danger')
            return render_template('contact.html', page_active='contact',name=name,message=message,email_address=email_address,subject=subject,csrf_token=csrf_token)
        
        if not validate_email.validate_email(email_address):
            flash('You must enter a valid email address.', 'danger')
            return render_template('contact.html', page_active='contact',name=name,message=message,email_address=email_address,subject=subject,csrf_token=csrf_token)
        
        # Escape all of the variables:
        name = name.replace("<", "&lt;")
        name = name.replace(">", "&gt;")

        subject = subject.replace("<", "&lt;")
        subject = subject.replace(">", "&gt;")

        message = message.replace("<", "&lt;")
        message = message.replace(">", "&gt;")

        # Generate the message body
        message_body = """A message was received from the go-cart.io contact form.

Name:       {}
Email:      {}
Subject:    {}

Message:

{}""".format(name, email_address, subject, message)

        mime_message = email.mime.text.MIMEText(message_body)
        mime_message['Subject'] = "go-cart.io Contact Form: " + subject
        mime_message['From'] = settings.SMTP_FROM_EMAIL
        mime_message['To'] = settings.SMTP_DESTINATION

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:

                if settings.SMTP_AUTHENTICATION_REQUIRED:
                    smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

                smtp.send_message(mime_message)

                smtp.quit()
        # For some reason connect doesn't catch the socket error
        # *sigh*
        except (smtplib.SMTPException,socket.gaierror):
            flash('There was an error sending your message.', 'danger')
            return render_template('contact.html', page_active='contact',name=name,message=message,email_address=email_address,subject=subject,csrf_token=csrf_token)

        flash('Your message was successfully sent.', 'success')
        return redirect(url_for('contact'))

@app.route('/cart/<string_key>', methods=['GET'])
def cartogram_by_key(string_key):

    cartogram_entry = CartogramEntry.query.filter_by(string_key=string_key).first_or_404()

    if cartogram_entry.handler not in cartogram_handlers:
        return Response('Error', status=500)
    
    cartogram_handlers_select = [{'id': key, 'display_name': handler.get_name()} for key, handler in cartogram_handlers.items()]

    return render_template('new_cartogram.html', page_active='home',cartogram_url=url_for('cartogram'), cartogramui_url=url_for('cartogram_ui'), cartogram_data_dir=url_for('static', filename='cartdata'), cartogram_handlers=cartogram_handlers_select, default_cartogram_handler=cartogram_entry.handler, cartogram_data=cartogram_entry.cartogram_data, cartogramui_data=cartogram_entry.cartogramui_data)
    


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
        json_response['grid_document'] = cart_data[3]

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

    # This function returns a generator used by Flask to generate a streaming HTTP response.
    # It uses output from stderr to determine the generation progress (particularly the value 'max abs. error')
    # When generation is done, it returns the .gen output converted into JSON by gen2dict
    def generate_streamed_json_response():

        cartogram_gen_output = b''
        current_loading_point = "null"

        # We have to format our JSON manually, since we're not sending a complete object.
        # On the client side, Oboe.js is intelligent enough to parse this and get the loading information and cartogram output
        yield '{"loading_progress_points":['

        for source, line in cartwrap.generate_cartogram(cartogram_handler.gen_area_data(values), cartogram_handler.get_gen_file(), "{}/cartogram".format(settings.CARTOGRAM_DATA_DIR)):

            if source == "stdout":
                cartogram_gen_output += line
            else:
                s = re.search(r'max\. abs\. area error: (.+)', line.decode())

                if s != None:
                    current_loading_point = s.groups(1)[0]
                
                # We always include the loading progress, even if it hasn't changed.
                # This makes life easier on the client side
                yield '{{"loading_point": {}, "stderr_line": "{}"}},'.format(current_loading_point, line.decode())
        
        # We create a fake last entry because you can't have dangling commas in JSON
        yield '{"loading_point":0, "stderr_line": ""}],"cartogram_data":'

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

