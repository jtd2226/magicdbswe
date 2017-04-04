import logging

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgresql+psycopg2://magicdb:mtgdb@127.0.0.1:5432/postgres'
db.init_app(app)

@app.route('/')
@app.route('/index')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

#--------CARDS------------
@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/cards/<name>')
def cards_instance(name):
    #cards_instance = #QueryHere
    return render_template()

#Cards_instance

#--------ARTISTS----------
@app.route('/artists')
def artists():
    return render_template('artists.html')

#artists_instance

#--------SETS--------------
@app.route('/sets')
def sets():
    return render_template('sets.html')


#sets_instance

#-------SUBTYPES-----------
@app.route('/subtypes')
def subtpes():
    return render_template('subtypes.html')

#subtypes_instance

@app.route('/form')
def form():
        return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
        name = request.form['name']
        email = request.form['email']
        site = request.form['site_url']
        comments = request.form['comments']
        return render_template(
                    'submitted_form.html',
                    name=name,
                    email=email,
                    site=site,
                    comments=comments
                )

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
