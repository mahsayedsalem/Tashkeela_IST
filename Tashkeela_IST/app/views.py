"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from .models import User
import os
from .Shakkala import Shakkala
from keras import backend as K

import tensorflow as tf
# import sqlite3

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/add-tashkeela', methods=['POST', 'GET'])
def add_tashkeela():
    if request.method == 'POST':

        input_text = request.form['inputText']
        final_output = 'يرجى إدخال النص في الخانة السابقة'
        if input_text != "":
            folder_location = os.path.dirname(os.path.abspath(__file__))
            sh = Shakkala(folder_location)
            input_int = sh.prepare_input(input_text)
            K.clear_session()
            model, graph = sh.get_model()
            with graph.as_default():
                logits = model.predict(input_int)[0]
            predicted_harakat = sh.logits_to_text(logits)
            final_output = sh.get_final_text(input_text, predicted_harakat)

        return render_template('add_tashkeela.html', outputText = final_output, inputText = input_text)
    return render_template('add_tashkeela.html', outputText="", inputText="")

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


