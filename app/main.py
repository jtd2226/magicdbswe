import logging

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#?unix_socket=/cloudsql/tutorial-project-161522:us-central1:magicinstance
#?host=/cloudsql/tutorial-project-161522:us-central1:magicinstance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://magicdb:mtgdb@35.188.87.113:5432/magicdb'
db = SQLAlchemy(app)

import models

@app.route('/')
@app.route('/index')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test')
def test():
    text = models.Test.query.all()
    return render_template('test.html',text=text)

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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
