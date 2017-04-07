#
# A Database for Magic the Gathering Cards
#
# pylint:disable=invalid-name,line-too-long,no-member,too-few-public-methods,locally-disabled
import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
with app.app_context():
	db.init_app(app)


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    init_app(app)				#added "db."
    with app.app_context():
        db.create_all()
    print("All tables created")

if __name__ == '__main__':
    _create_database()

STG_LEN = 12
NAME_LEN = 32
SHORT_LEN = 128
MED_LEN = 256
TEXT_LEN = 1024


"""
Handling many-to-many relations
"""
subtype_table = db.Table('subtype_table',
    db.Column('subtype_name', db.String(MED_LEN), db.ForeignKey('subtypes.name')),
    db.Column('card_id', db.String(TEXT_LEN), db.ForeignKey('cards.cardId'))
)

set_artist_table = db.Table('set_artist_table',
	db.Column('set_code', db.String(STG_LEN), db.ForeignKey('sets.code')),
	db.Column('artist_name', db.String(MED_LEN), db.ForeignKey('artists.name'))
)

set_subtype_table = db.Table('set_subtype_table',
    db.Column('subtype_name', db.String(MED_LEN), db.ForeignKey('subtypes.name')),
    db.Column('set_code', db.String(STG_LEN), db.ForeignKey('sets.code'))
)

class MCard(db.Model):

	"""
	Information regarding specific cards

	cardId = Unique ID to identify a card
	name = Name of the card
	mainType = Primary Type of the Card
	subType = Secondary Type(s) of the Card
	text = All of the text written on the card
	expansionSet = The set under which the card came out
	manaCost = The Converted Mana Cost of the card
	color = The color(s) of which the card is a part of
	power = Power of the card (if creature)
	toughness = Toughness of the card (if creature)
	art = Link to the image of the card
	rarity = Rarity of the card
	artist = Artist that made the card art
	"""

	__tablename__ = 'cards'

	#Relevant attributes for a card
	cardId = db.Column(db.String(TEXT_LEN), primary_key=True)
	name = db.Column(db.String(MED_LEN))
	mainType = db.Column(db.String(NAME_LEN))
	subType = db.relationship('MSubtype', secondary=subtype_table, backref=db.backref('xcards', lazy='dynamic'))
	text = db.Column(db.String(TEXT_LEN), nullable=True)
	expansionSet = db.Column(db.String(STG_LEN), db.ForeignKey('sets.code'))
	manaCost = db.Column(db.Integer, nullable=True)
	color = db.Column(db.String(SHORT_LEN), nullable=True)
	power = db.Column(db.String(SHORT_LEN), nullable=True)
	toughness = db.Column(db.String(SHORT_LEN), nullable=True)
	art = db.Column(db.String(MED_LEN))
	rarity = db.Column(db.String(STG_LEN))
	artist = db.Column(db.String(MED_LEN), db.ForeignKey('artists.name'))

	def __init__(self, cardId, name, mainType, subType, text, expansionSet,
				 manaCost, color, power, toughness, art, rarity, artist):
		self.cardId = cardId
		self.name = name
		self.mainType = mainType
		self.subType = subType
		self.text = text
		self.expansionSet = expansionSet
		self.manaCost = manaCost
		self.color = color
		self.power = power
		self.toughness = toughness
		self.art = art
		self.rarity = rarity
		self.artist = artist

	def __repr__(self):
		return '<MCard %r>' % self.name

class MSet(db.Model):
	"""
	Information regarding card sets (A.K.A.: expansions)

	code = ID by which expansions can be identified
	name = Name of the expansions
	rDate = Release Date of the expansions
	block = Block that the expansion belongs to
	cards = Cards from this expansion
	subTypes = All subtypes in the expansion
	numCards = Number of cards that came out in the expansion
	symbol = Symbol used to identify the expansion on cards
	xartists = Artists that made cards for this expansion
	"""

	__tablename__ = 'sets'

	code = db.Column(db.String(STG_LEN), primary_key=True)
	name = db.Column(db.String(MED_LEN))
	rDate = db.Column(db.String(NAME_LEN))
	block = db.Column(db.String(NAME_LEN), nullable=True)
	cards = db.relationship('MCard', backref='set', lazy='dynamic')
	numCards = db.Column(db.Integer)
	symbol = db.Column(db.String(MED_LEN)) #link
	subTypes = db.relationship('MSubtype', secondary=set_subtype_table, backref=db.backref('ssets', lazy='dynamic'))

	def __init__(self, code, name, rDate, block, numCards,
				 symbol, subTypes):
		self.code = code
		self.name = name
		self.rDate = rDate
		self.block = block
		self.numCards = numCards
		self.symbol = symbol
		self.subTypes = subTypes

	def __repr__(self):
		return '<MSet %r>' % self.code

class MArtist(db.Model):
	"""
	Information regarding artists of MtG cards

	name = Name of artist
	numCards = Number of cards this artist has worked on
	numSets = Number of Sets this artist has worked on
	cards = Cards that this artist has worked on
	sets = Sets that this artist has worked on
	"""

	__tablename__ = 'artists'

	#Possibility of repeated names
	name = db.Column(db.String(MED_LEN), primary_key=True)
	numCards = db.Column(db.Integer)
	numSets = db.Column(db.Integer)
	cards = db.relationship('MCard', backref='artistboi', lazy='dynamic')
	sets = db.relationship('MSet', secondary=set_artist_table, backref=db.backref('xartists', lazy='dynamic'))

	def __init__(self, name, numCards, numSets, sets):
		self.name = name
		self.numCards = numCards
		self.numSets = numSets
		self.sets = sets

	def __repr__(self):
		return '<MArtist %r>' % self.name

class MSubtype(db.Model):
	"""
	Information regarding types

	name = Name of the subtype
	numCards = Number of existing cards of this subtype
	xcards = cards that are of this subtype
	ssets = Sets that contain cards of this subtype
	"""

	__tablename__ = 'subtypes'

	name = db.Column(db.String(MED_LEN), primary_key=True)
	numCards = db.Column(db.Integer) 

	def __init__(self, name, numCards):
		self.name = name
		self.numCards = numCards

	def __repr__(self):
		return '<MSubtype %r>' % self.name
