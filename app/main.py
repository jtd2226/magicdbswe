import logging
import config
import models

from config import POSTS_PER_PAGE
from models import db, app, MSubtype, MCard, MArtist, MSet
from flask import Flask, render_template, request, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination # make sure to pyhton3 -m pip install

#app = Flask(__name__)

#?unix_socket=/cloudsql/tutorial-project-161522:us-central1:magicinstance
#?host=/cloudsql/tutorial-project-161522:us-central1:magicinstance

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://magicdb:mtgdb@35.188.87.113:5432/magicdb'

# with app.app_context():
#         model = models
#         model.init_app(app)


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
    output = subprocess.run(['make','test', '-C', '../'], stdout = subprocess.PIPE).stdout.decode('utf-8')
    output = "<br />".join(output.split("\n"))
    output = Markup(output)
    return render_template('run-tests.html', output = output, title = 'Run Tests')

#--------CARDS------------
@app.route('/cards')
@app.route('/cards/<int:page>')
def cards(page=1):
    #cards = db.session.query(MCard).all()
    cards = db.session.query(MCard).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('cards.html',cards=cards, title = 'Cards')

# ****** Pagination required
@app.route('/cards/<name>')
#@app.route('/cards/<name>/<int:page>')
def cards_instance(name):
    #cards_instance = models.MCard.query.filter_by(name=name).first()
    return render_template('cards-instance.html',cards_instance=cards_instance, title = name)


#--------ARTISTS----------
@app.route('/artists')
@app.route('/artists/<int:page>')
def artists(page=1):
    #artists = db.session.query(MArtist).all()
    artists = db.session.query(MArtist).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('artists.html',artists=artists, title = 'Artists')

@app.route('/artists/<name>')
def artists_instance(name):
    cards_instance = models.MArtist.query.filter_by(name=name).first()
    return render_template('artists-instance.html',artists_instance=artists_instance, title = name)



#--------SETS--------------
@app.route('/sets')
@app.route('/sets/<int:page>')
def sets(page=1):
    #sets = db.session.query(MSet).all()
    sets = db.session.query(MSet).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('sets.html',sets=sets, title = 'Sets')

@app.route('/sets/filter/<relYear>&<numCard>')
def sets_filter(relYear, numCard, page=1):
    sets = db.session.query(MSet);
    if relYear != "NO-RELYEAR":
        sets = sets.filter_by(rDate=relYear)
    if numCard != "NO-NUMCARD":
        sets = sets.filter_by(numCards=numCard)

    #sets = sets.all()
    sets = sets.paginate(page, POSTS_PER_PAGE, False).items

    imageUrls = {}
    #for set in sets:
    #   imageUrls[set.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art

    return render_template('sets.html', sets=sets, title = 'Subtypes')


@app.route('/sets/<name>')
def sets_instance(name):
    sets_instance = db.session.query(MSet).filter_by(name=name).first()
    return render_template('sets-instance.html',sets_instance=sets_instance, title = name)




#-------SUBTYPES-----------
# @app.route('/', methods=['GET', 'POST'])
@app.route('/subtypes') #included for pagination
@app.route('/subtypes/<int:page>') #included for pagination
# @app.route('/subtypes')
# @app.route('/subtypes/')
@app.route('/subtypes/filter')
@app.route('/subtypes/sort')
def subtypes(page = 1):
    #subtypes = db.session.query(MSubtype).all()
    subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items #included for pagination
    #Get Images
    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=253575&type=card"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls)

@app.route('/subtypes/sort/<field>&<order>')
@app.route('/subtypes/sort/<field>&<order>/<int:page>')
def subtypes_sort(field, order, page=1):
    if "desc" in order : # Descending Order
        if field == "name" :
            #subtypes = db.session.query(MSubtype).all()
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            #subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards).all()
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            #subtypes = db.session.query(MSubtype).all
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
            subtypes.sort(key=lambda x: len(x.ssets.all()))
    else : # Ascending Order
        if field == "name" :
            #subtypes = db.session.query(MSubtype).order_by(MSubtype.name.desc()).all()
            subtypes = db.session.query(MSubtype).order_by(MSubtype.name.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            #subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards.desc()).all()
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            #subtypes = db.session.query(MSubtype).all()
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
            subtypes.sort(key=lambda x: len(x.ssets.all()), reverse=True)

    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=253575&type=card"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls)

@app.route('/subtypes/filter/<numCards>&<numSets>&<setName>')
@app.route('/subtypes/filter/<numCards>&<numSets>&<setName>/<int:page>')
def subtypes_filter(numCards, numSets, setName, page=1):
    subtypes = None
    intNumSets = 0

    #VAriables
    try: #Verify that a real number is passed
        int(numCards)
    except ValueError:
        numCards="NO-NUMCARD"

    try: #Verify that a real number is passed
        intNumSets = int(numSets)
    except ValueError:
        numSets = "NO-NUMSETS"

    setName = setName.replace("%20", " ").replace("%2C", "")


    if numCards != "NO-NUMCARD": #NumCard Filter
        #subtypes = db.session.query(MSubtype).filter_by(numCards=numCards).all()
        subtypes = db.session.query(MSubtype).filter_by(numCards=numCards).paginate(page, POSTS_PER_PAGE, False).items
    if numSets != "NO-NUMSETS": #NumSet Filter
        if numCards == "NO-NUMCARD":
            #subtypes = db.session.query(MSubtype).all()
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
        newsub = []
        for subtype in subtypes:
            #curr_sets = db.session.query(MSubtype).filter_by(name=subtype.name).first().ssets.all()
            curr_sets = db.session.query(MSubtype).filter_by(name=subtype.name).first().ssets.paginate(page, POSTS_PER_PAGE, False).items
            if len(curr_sets) == intNumSets:
                newsub.append(subtype)
        subtypes = newsub
    if setName != "NO-SETNAME": #SetName Filter
        if numCards == "NO-NUMCARD" and numSets == "NO-NUMSETS":
            #subtypes = db.session.query(MSubtype).all()
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items

        print(str(len(subtypes)))
        for subtype in subtypes:
            isInSets = False
            print(subtype.name)
            #curr_sets = db.session.query(MSubtype).filter_by(name=subtype.name).first().ssets.all()
            curr_sets = db.session.query(MSubtype).filter_by(name=subtype.name).first().ssets.paginate(page, POSTS_PER_PAGE, False).items
            for cset in curr_sets:
                if cset.code == setName :
                    isInSets = True
                    break
            if not isInSets:
                subtypes.remove(subtype)

    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=253575&type=card"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls)

@app.route('/subtypes/<name>')
def subtypes_instance(name):
    subtypes_instance = db.session.query(MSubtype).filter_by(name=name).first()

    subtypeImageUrls = ""
    if db.session.query(MSubtype).filter_by(name=subtypes_instance.name).first().xcards.first():
        subtypeImageUrls = db.session.query(MSubtype).filter_by(name=subtypes_instance.name).first().xcards.first().art
    else:
        subtypeImageUrls = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=253575&type=card"

    return render_template('subtypes-instance.html',subtypes_instance=subtypes_instance, title = name, imageUrls=subtypeImageUrls)

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
