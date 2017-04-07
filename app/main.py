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


@app.route('/run-tests')
def run_tests():
    import subprocess
    #output = subprocess.run(['python3', 'TestMagic.py'], stdout = subprocess.PIPE).stdout.decode()
    return render_template('run-tests.html', title = 'Run Tests')

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
    artists = db.session.query(MArtist).all()
    return render_template('artists.html',artists=artists, title = 'Artists')

@app.route('/artists/<name>')
def artists_instance(name):
    cards_instance = models.MArtist.query.filter_by(name=name).first()
    return render_template('artists-instance.html',artists_instance=artists_instance, title = name)



#--------SETS--------------
@app.route('/sets')
def sets():
    sets = db.session.query(MSet).all()
    return render_template('sets.html',sets=sets, title = 'Sets')

@app.route('/sets/filter/<relYear>&<numCard>')
def sets_filter(relYear, numCard):
    sets = db.session.query(MSet);
    if relYear != "NO-RELYEAR":
        sets = sets.filter_by(rDate=relYear)
    if numCard != "NO-NUMCARD":
        sets = sets.filter_by(numCards=numCard)

    sets = sets.all()

    imageUrls = {}
    #for set in sets:
    #   imageUrls[set.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art

    return render_template('sets.html', sets=sets, title = 'Subtypes',)


@app.route('/sets/<name>')
def sets_instance(name):
    sets_instance = db.session.query(MSet).filter_by(name=name).first()
    return render_template('sets-instance.html',sets_instance=sets_instance, title = name)




#-------SUBTYPES-----------
@app.route('/subtypes')
def subtypes():
    subtypes = db.session.query(MSubtype).all()
    imageUrls = {}
    #for subtype in subtypes:
    #   imageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=imageUrls)

@app.route('/subtypes/sort/<field>&<order>')
def subtypes_sort(field, order):
    if "desc" in order : # Descending Order
        if field == "name" :
            subtypes = db.session.query(MSubtype).all()
        elif field == "numCards" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards).all()
        elif field == "numSets" :
            subtypes = db.session.query(MSubtype).all()#fix
    else : # Ascending Order
        if field == "name" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.name.desc()).all()
        elif field == "numCards" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards.desc()).all()
        elif field == "numSets" :
            subtypes = db.session.query(MSubtype).all()#fix

    imageUrls = {}
    #for subtype in subtypes:
    #   imageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=imageUrls)

@app.route('/subtypes/filter/<numCards>&<numSets>&<setName>')
def subtypes_filter(numCards, numSets, setName):
    subtypes = db.session.query(MSubtype);
    if numCards != "NO-NUMCARD":
        subtypes = subtypes.filter_by(numCards=numCards)
    if numSets != "NO-NUMSETS":
        pass
    if setName != "NO-SETNAME":
        pass

    subtypes = subtypes.all()

    imageUrls = {}
    #for subtype in subtypes:
    #   imageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=imageUrls)

@app.route('/subtypes/<name>')
def subtypes_instance(name):
    subtypes_instance = db.session.query(MSubtype).filter_by(name=name).first()
    return render_template('subtypes-instance.html',subtypes_instance=subtypes_instance, title = name)

@app.route('/cool')
def test():
    return render_template('cool.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
