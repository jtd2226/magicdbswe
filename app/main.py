import logging
import config
import models

from config import POSTS_PER_PAGE
from models import db, app, MSubtype, MCard, MArtist, MSet, Resource, api
from flask import Flask, render_template, request, Markup, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination # make sure to pyhton3 -m pip install
from collections import OrderedDict

#-------
#  API
#-------
class Api_Cards(Resource):
    def get(self):
        apidict = list()
        for c in db.session.query(MCard).all():
            apidict.append(c.cardId)
        return jsonify(apidict)


class Api_Card(Resource):
    def get(self, id):
        apicard = db.session.query(MCard).filter_by(cardId=id).first()
        apilist = list()
        for s in apicard.subType:
            apilist.append(s.name)

        return jsonify({"cardId": apicard.cardId, "name": apicard.name, "mainType": apicard.mainType,"subType": apilist, "text": apicard.text, "expansionSet": apicard.expansionSet,"manaCost": apicard.manaCost, "color": apicard.color, "power": apicard.power,"toughness": apicard.toughness,
        "art": apicard.art,"rarity": apicard.rarity, "artist": apicard.artist})


api.add_resource(Api_Cards,'/api/cards')
api.add_resource(Api_Card,'/api/cards/<string:id>')

class Api_Sets(Resource):
    def get(self):
        apidict = list()
        for s in db.session.query(MSet).all():
            apidict.append(s.code)
        return jsonify(apidict)

class Api_Set(Resource):
    def get(self, code):
        apiset = db.session.query(MSet).filter_by(code=code).first()
        cl = list()
        for s in apiset.cards:
            cl.append(s.cardId)
        sl = list()
        for s in apiset.subTypes:
            sl.append(s.name)
        al = list()
        for s in apiset.xartists:
            al.append(s.name)
        return jsonify({"code": apiset.code, "name": apiset.name, "rDate": apiset.rDate,
         "block": apiset.block, "cards": cl, "subTypes": sl, "numCards": apiset.numCards, "symbol": apiset.symbol, "artists": al})

api.add_resource(Api_Sets, '/api/sets')
api.add_resource(Api_Set, '/api/sets/<string:code>')

class Api_Artists(Resource):
    def get(self):
        apilist = list()
        for apiart in db.session.query(MArtist).all():
            cl = [s.cardId for s in apiart.cards]
            sl = [s.code for s in apiart.sets]
            apilist.append({"name": apiart.name, "numCards": apiart.numCards, "numSets": apiart.numSets,
            "cards": cl, "sets": sl})
        return jsonify(apilist)

api.add_resource(Api_Artists, '/api/artists')

class Api_Subtypes(Resource):
    def get(self):
        apilist = list()
        for apist in db.session.query(MSubtype).all():
            cl = [s.cardId for s in apist.xcards]
            sl = [s.code for s in apist.ssets]
            apilist.append({"name": apist.name, "numCards": apist.numCards,
            "numSets": apist.numSets, "cards": cl, "sets": sl})
        return jsonify(apilist)

api.add_resource(Api_Subtypes, '/api/subtypes')

def get_page_url(curr_url, new_page):
    try:
        newrl = curr_url.split("/")
        int(newrl[-1])
        newrl[-1] = str(new_page)

        return "/".join(newrl).replace(" ", "%20")
    except ValueError:
        return curr_url + "/" + str(new_page)

def cmp_to_key(mycmp):
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def rarity_cmp(x, y):
    return get_rarity_val(x) - get_rarity_val(y)

def get_rarity_val(card):
    rarity = card.rarity.lower()
    if rarity == "mythic rare":
        return 5
    if rarity == "special":
        return 4
    if rarity == "rare":
        return 3
    if rarity == "uncommon":
        return 2
    if rarity == "common":
        return 1
    if rarity == "basic land":
        return 0
    return -1

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
    output = subprocess.run(['make'], stdout = subprocess.PIPE).stdout.decode('utf-8')
    output = "<br />".join(output.split("\n"))
    output = Markup(output)
    return render_template('run-tests.html', output = output, title = 'Run Tests')

#--------CARDS------------
@app.route('/cards')
@app.route('/cards/<int:page>')
def cards(page=1):
    cards = db.session.query(MCard).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('cards.html',cards=cards, title = 'Cards', page=page, get_page_url=get_page_url)

@app.route('/cards/sort/<field>&<order>')
@app.route('/cards/sort/<field>&<order>/<int:page>')
def cards_sort(field, order, page=1):
    if "desc" in order : # Descending Order
        if field == "name" :
            cards = db.session.query(MCard).order_by(MCard.name).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "manaCost" :
            cards = db.session.query(MCard).order_by(MCard.manaCost).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "power" :
            cards = db.session.query(MCard).order_by(MCard.power).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "toughness" :
            cards = db.session.query(MCard).order_by(MCard.toughness).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "rarity" :
            cards = sorted(db.session.query(MCard).order_by(MCard.rarity).all(), key=cmp_to_key(rarity_cmp))[(page - 1) * POSTS_PER_PAGE : page * POSTS_PER_PAGE]
        elif field == "color" :
            cards = db.session.query(MCard).order_by(MCard.color).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "type" :
            cards = db.session.query(MCard).order_by(MCard.mainType).paginate(page, POSTS_PER_PAGE, False).items
    else : # Ascending Order
        if field == "name" :
            cards = db.session.query(MCard).order_by(MCard.name.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "manaCost" :
            cards = db.session.query(MCard).order_by(MCard.manaCost.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "power" :
            cards = db.session.query(MCard).order_by(MCard.power.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "toughness" :
            cards = db.session.query(MCard).order_by(MCard.toughness.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "rarity" :
            cards = sorted(db.session.query(MCard).order_by(MCard.rarity).all(), key=cmp_to_key(rarity_cmp), reverse=True)[(page - 1) * POSTS_PER_PAGE : page * POSTS_PER_PAGE]
        elif field == "color" :
            cards = db.session.query(MCard).order_by(MCard.color.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "type" :
            cards = db.session.query(MCard).order_by(MCard.mainType.desc()).paginate(page, POSTS_PER_PAGE, False).items

    return render_template('cards.html', cards=cards, title = 'Cards', page=page, get_page_url=get_page_url)

@app.route('/cards/filter/<manaCost>&<power>&<toughness>&<rarity>&<color>&<mainType>')
@app.route('/cards/filter/<manaCost>&<power>&<toughness>&<rarity>&<color>&<mainType>/<int:page>')
def cards_filter(manaCost, power, toughness, rarity, color, mainType, page=1):
    cards = db.session.query(MCard);
    if manaCost != "NO-MANA":
        cards = cards.filter_by(manaCost=manaCost)
    if power != "NO-POWER":
        cards = cards.filter_by(power=power)
    if toughness != "NO-TOUGH":
        cards = cards.filter_by(toughness=toughness)
    if rarity != "NO-RARITY":
        cards = cards.filter_by(rarity=rarity)
    if color != "NO-COLOR":
        color = color.capitalize()
        cards = cards.filter_by(color=color)
    if mainType != "NO-TYPE":
        cards = cards.filter_by(mainType=mainType)

    cards = cards.paginate(page, POSTS_PER_PAGE, False).items

    return render_template('cards.html', cards=cards, title = 'Cards', page=page, get_page_url=get_page_url)

@app.route('/cards/<cardId>')
def cards_instance(cardId):
    cards_instance = db.session.query(MCard).filter_by(cardId=cardId).first()
    return render_template('cards-instance.html',cards_instance=cards_instance, title = cards_instance.name)


#--------ARTISTS----------
@app.route('/artists')
@app.route('/artists/<int:page>')
def artists(page=1):
    artists = db.session.query(MArtist).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('artists.html', artists=artists, title = 'Artists', page=page, get_page_url=get_page_url)


@app.route('/artists/filter/<numCard>&<numSets>')
@app.route('/artists/filter/<numCard>&<numSets>/<int:page>')
def artists_filter(numCard, numSets, page=1):
    artists = db.session.query(MArtist);
    if numCard != "NO-NUMCARD":
        artists = artists.filter_by(numCards=numCard)
    if numSets != "NO-NUMSETS":
        artists = artists.filter_by(numSets=numSets)

    artists = artists.paginate(page, POSTS_PER_PAGE, False).items

    return render_template('artists.html', artists=artists, title = 'Artists', page=page, get_page_url=get_page_url)

@app.route('/artists/sort/<field>&<order>')
@app.route('/artists/sort/<field>&<order>/<int:page>')
def artists_sort(field, order, page=1):
    if "desc" in order : # Descending Order
        if field == "name" :
            artists = db.session.query(MArtist).order_by(MArtist.name).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            artists = db.session.query(MArtist).order_by(MArtist.numCards).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            artists = db.session.query(MArtist).order_by(MArtist.numSets).paginate(page, POSTS_PER_PAGE, False).items
    else : # Ascending Order
        if field == "name" :
            artists = db.session.query(MArtist).order_by(MArtist.name.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            artists = db.session.query(MArtist).order_by(MArtist.numCards.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            artists = db.session.query(MArtist).order_by(MArtist.numSets.desc()).paginate(page, POSTS_PER_PAGE, False).items

    return render_template('artists.html', artists=artists, title = 'Artists', page=page, get_page_url=get_page_url)

@app.route('/artists&name="<name>"')
def artists_instance(name):
    artists_instance = db.session.query(MArtist).filter_by(name=name).first()
    return render_template('artists-instance.html',artists_instance=artists_instance, title = name)

#--------SETS--------------
@app.route('/sets')
@app.route('/sets/<int:page>')
def sets(page=1):
    sets = db.session.query(MSet).paginate(page, POSTS_PER_PAGE, False).items
    return render_template('sets.html',sets=sets, title = 'Sets', page=page, get_page_url=get_page_url)

@app.route('/sets/filter/<relYear>&<numCard>')
@app.route('/sets/filter/<relYear>&<numCard>/<int:page>')
def sets_filter(relYear, numCard, page=1):
    sets = db.session.query(MSet);
    if relYear != "NO-RELYEAR":
        sets = sets.filter_by(rDate=relYear)
    if numCard != "NO-NUMCARD":
        sets = sets.filter_by(numCards=numCard)

    sets = sets.paginate(page, POSTS_PER_PAGE, False).items

    return render_template('sets.html', sets=sets, title = 'Sets', page=page, get_page_url=get_page_url)

@app.route('/sets/sort/<field>&<order>')
@app.route('/sets/sort/<field>&<order>/<int:page>')
def sets_sort(field, order, page=1):
    if "desc" in order : # Descending Order
        if field == "name" :
            sets = db.session.query(MSet).order_by(MSet.name).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "code" :
            sets = db.session.query(MSet).order_by(MSet.code).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "relDate" :
            sets = db.session.query(MSet).order_by(MSet.rDate).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            sets = db.session.query(MSet).order_by(MSet.numCards).paginate(page, POSTS_PER_PAGE, False).items
    else : # Ascending Order
        if field == "name" :
            sets = db.session.query(MSet).order_by(MSet.name.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "code" :
            sets = db.session.query(MSet).order_by(MSet.code.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "relDate" :
            sets = db.session.query(MSet).order_by(MSet.rDate.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            sets = db.session.query(MSet).order_by(MSet.numCards.desc()).paginate(page, POSTS_PER_PAGE, False).items

    return render_template('sets.html', sets=sets, title = 'Sets', page=page, get_page_url=get_page_url)

@app.route('/sets/<code>')
def sets_instance(code):
    sets_instance = db.session.query(MSet).filter_by(code=code).first()
    return render_template('sets-instance.html', sets_instance=sets_instance, title = sets_instance.name)




#-------SUBTYPES-----------
# @app.route('/', methods=['GET', 'POST'])
@app.route('/subtypes')
@app.route('/subtypes/<int:page>') #included for pagination
def subtypes(page = 1):
    subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items #included for pagination
    #Get Images
    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls, page=page, get_page_url=get_page_url)

@app.route('/subtypes/sort/<field>&<order>')
@app.route('/subtypes/sort/<field>&<order>/<int:page>')
def subtypes_sort(field, order, page=1):
    if "desc" in order : # Descending Order
        if field == "name" :
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numSets).paginate(page, POSTS_PER_PAGE, False).items
    else : # Ascending Order
        if field == "name" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.name.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numCards" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numCards.desc()).paginate(page, POSTS_PER_PAGE, False).items
        elif field == "numSets" :
            subtypes = db.session.query(MSubtype).order_by(MSubtype.numSets.desc()).paginate(page, POSTS_PER_PAGE, False).items

    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls, page=page, get_page_url=get_page_url)

@app.route('/subtypes/filter/<numCards>&<numSets>&<setName>')
@app.route('/subtypes/filter/<numCards>&<numSets>&<setName>/<int:page>')
def subtypes_filter(numCards, numSets, setName, page=1):
    subtypes = None
    intNumSets = 0

    #Variables
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
        subtypes = db.session.query(MSubtype).filter_by(numCards=numCards).paginate(page, POSTS_PER_PAGE, False).items
    if numSets != "NO-NUMSETS": #NumSet Filter
        if numCards == "NO-NUMCARD":
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items
        newsub = []
        for subtype in subtypes:
            curr_sets = db.session.query(MSubtype).filter_by(name=subtype.name).first().ssets.paginate(page, POSTS_PER_PAGE, False).items
            if len(curr_sets) == intNumSets:
                newsub.append(subtype)
        subtypes = newsub
    if setName != "NO-SETNAME": #SetName Filter
        if numCards == "NO-NUMCARD" and numSets == "NO-NUMSETS":
            subtypes = db.session.query(MSubtype).paginate(page, POSTS_PER_PAGE, False).items

        print(str(len(subtypes)))
        for subtype in subtypes:
            isInSets = False
            print(subtype.name)
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
            subtypeImageUrls[subtype.name] = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    return render_template('subtypes.html', subtypes=subtypes, title = 'Subtypes', imageUrls=subtypeImageUrls, page=page, get_page_url=get_page_url)

@app.route('/subtypes/<name>')
def subtypes_instance(name):
    subtypes_instance = db.session.query(MSubtype).filter_by(name=name).first()

    subtypeImageUrls = ""
    if db.session.query(MSubtype).filter_by(name=subtypes_instance.name).first().xcards.first():
        subtypeImageUrls = db.session.query(MSubtype).filter_by(name=subtypes_instance.name).first().xcards.first().art
    else:
        subtypeImageUrls = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    return render_template('subtypes-instance.html',subtypes_instance=subtypes_instance, title = name, imageUrls=subtypeImageUrls)

@app.route('/cool')
def test():
    return render_template('cool.html')
    
@app.route('/visualization')
def visualization():
    return render_template('visualization.html', title = 'Visualization of ggnoswe')

#-------SEARCH-----------
@app.route('/search/cards/<searchText>')
@app.route('/search/cards/<searchText>/<int:page>')
@app.route('/search/<searchText>')
@app.route('/search/<searchText>/<int:page>')
def card_search(searchText, page=1):
    cards_tracker = {}
    or_cards_tracker = {}
    original_cards = db.session.query(MCard);

    for c in original_cards:
        if (searchText.lower() in c.name.lower()) or (searchText.lower() in c.mainType.lower()):
            cards_tracker[c.cardId] = c

        for word in searchText.lower().split():
            if (word in c.name.lower()) or (word in c.mainType.lower()):
                or_cards_tracker[c.cardId] = c

    cards_lo_index = max(0, (page - 1) * POSTS_PER_PAGE) #The low index is inclusive!
    cards_hi_index = min(len(cards_tracker), page * POSTS_PER_PAGE) #The high index is exclusive!
  
    cards_tracker = OrderedDict(sorted(cards_tracker.items()))
    cards = list(cards_tracker.values())[cards_lo_index:cards_hi_index]

    or_cards_tracker = OrderedDict(sorted(or_cards_tracker.items()))
    or_cards = list(or_cards_tracker.values())[cards_lo_index:cards_hi_index]

    hasNextPage = (cards_hi_index < len(cards_tracker))

    return render_template('search-cards.html', searchText=searchText, cards = cards, get_page_url=get_page_url, page=page, hasNextPage = hasNextPage, title = 'Search')

@app.route('/search/sets/<searchText>')
@app.route('/search/sets/<searchText>/<int:page>')
def set_search(searchText, page=1):
    sets_tracker = {}
    original_sets = db.session.query(MSet);

    for s in original_sets:
        if (searchText.lower() in s.name.lower()) or (searchText.lower() in s.code.lower()):
            sets_tracker[s.code] = s

    sets_lo_index = max(0, (page - 1) * POSTS_PER_PAGE) #The low index is inclusive!
    sets_hi_index = min(len(sets_tracker), page * POSTS_PER_PAGE) #The high index is exclusive!
    
    sets_tracker = OrderedDict(sorted(sets_tracker.items()))
    sets = list(sets_tracker.values())[sets_lo_index:sets_hi_index]

    hasNextPage = (sets_hi_index < len(sets_tracker))

    return render_template('search-sets.html', searchText=searchText, sets = sets, get_page_url=get_page_url, page=page, hasNextPage = hasNextPage, title = 'Search')

@app.route('/search/subtypes/<searchText>')
@app.route('/search/subtypes/<searchText>/<int:page>')
def subtype_search(searchText, page=1):
    subtypes_tracker = {}
    original_subtypes = db.session.query(MSubtype);

    for s in original_subtypes:
        if (searchText.lower() in s.name.lower()):
            subtypes_tracker[s.name] = s

    subtypes_lo_index = max(0, (page - 1) * POSTS_PER_PAGE) #The low index is inclusive!
    subtypes_hi_index = min(len(subtypes_tracker), page * POSTS_PER_PAGE) #The high index is exclusive!
    
    subtypes_tracker = OrderedDict(sorted(subtypes_tracker.items()))
    subtypes = list(subtypes_tracker.values())[subtypes_lo_index:subtypes_hi_index]

    hasNextPage = (subtypes_hi_index < len(subtypes_tracker))

    subtypeImageUrls = {}
    for subtype in subtypes:
        if db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first():
            subtypeImageUrls[subtype.name] = db.session.query(MSubtype).filter_by(name=subtype.name).first().xcards.first().art
        else:
            subtypeImageUrls[subtype.name] = "https://upload.wikimedia.org/wikipedia/en/a/aa/Magic_the_gathering-card_back.jpg"

    return render_template('search-subtypes.html', searchText=searchText, subtypes = subtypes, imageUrls=subtypeImageUrls, get_page_url=get_page_url, page=page, hasNextPage = hasNextPage, title = 'Search')

@app.route('/search/artists/<searchText>')
@app.route('/search/artists/<searchText>/<int:page>')
def artist_search(searchText, page=1):
    artists_tracker = {}
    original_artists = db.session.query(MArtist);

    for s in original_artists:
        if (searchText.lower() in s.name.lower()):
            artists_tracker[s.name] = s

    artists_lo_index = max(0, (page - 1) * POSTS_PER_PAGE) #The low index is inclusive!
    artists_hi_index = min(len(artists_tracker), page * POSTS_PER_PAGE) #The high index is exclusive!
    
    artists_tracker = OrderedDict(sorted(artists_tracker.items()))
    artists = list(artists_tracker.values())[artists_lo_index:artists_hi_index]

    hasNextPage = (artists_hi_index < len(artists_tracker))

    return render_template('search-artists.html', searchText=searchText, artists = artists, get_page_url=get_page_url, page=page, hasNextPage = hasNextPage, title = 'Search')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)