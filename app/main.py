import logging
import config
import models

from models import db, MSubtype, MCard, MArtist, MSet
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)

#?unix_socket=/cloudsql/tutorial-project-161522:us-central1:magicinstance
#?host=/cloudsql/tutorial-project-161522:us-central1:magicinstance

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://magicdb:mtgdb@35.188.87.113:5432/magicdb'

app = Flask(__name__)
app.config.from_object(config)
with app.app_context():
        model = models
        model.init_app(app)


@app.route('/')
@app.route('/index')
def hello():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html',title='About')


@app.route('/test')
def test():
    return render_template('test.html')

#--------CARDS------------
@app.route('/cards')
def cards():
    cards = models.MCard.query.all()
    return render_template('cards.html',cards=cards, title = 'Cards')

@app.route('/cards/<name>')
def cards_instance(name):
    #cards_instance = models.MCard.query.filter_by(name=name).first()
    return render_template('cards-instance.html',cards_instance=cards_instance, title = name)



#--------ARTISTS----------
@app.route('/artists')
def artists():
    artists = models.MArtist.query.all()
    return render_template('artists.html',artists=artists, title = 'Artists')

@app.route('/artists/<name>')
def artists_instance(name):
    cards_instance = models.MArtist.query.filter_by(name=name).first()
    return render_template('artists-instance.html',artists_instance=artists_instance, title = name)



#--------SETS--------------
@app.route('/sets')
def sets():
    #sets = models.MSets.query.all()
    return render_template('sets.html',sets=sets, title = 'Sets')


@app.route('/sets/<name>')
def sets_instance(name):
    cards_instance = models.MSets.query.filter_by(name=name).first()
    return render_template('sets-instance.html',sets_instance=sets_instance, title = name)




#-------SUBTYPES-----------
@app.route('/subtypes')
def subtypes():
    subtypes = db.session.query(MSubtype).filter_by(name="name").first()
    return render_template('subtypes.html',subtypes=subtypes, title = 'Subtypes')

@app.route('/subtypes/<name>')
def subtypes_instance(name):
    cards_instance = models.MSubtype.query.filter_by(name=name).first()
    return render_template('subtypes-instance.html',subtypes_instance=subtypes_instance, title = name)



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
