#
# A Database for Magic the Gathering Cards
#
# pylint:disable=invalid-name,line-too-long,no-member,too-few-public-methods,locally-disabled
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

STG_LEN = 12
NAME_LEN = 32
SHORT_LEN = 128
MED_LEN = 256
TEXT_LEN = 1024


db = SQLAlchemy()

def init_app(app):
	app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
	db.init_app(app)

class Test(db.Model):
	__tablename__ = 'Test'
  		  
	name = db.Column(db.String(MED_LEN), primary_key=True)

	def __init__(self,name):
		self.name = name
  		  
	def __repr__(self):
 		return '<Name %r>' % self.name

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()













# """
# Handling many-to-many relations
# """

# class Card(db.Model):

# 	"""
# 	Information regarding specific cards

# 	cardId = Unique ID to identify a card
# 	name = Name of the card
# 	mainType = Primary Type of the Card
# 	subType = Secondary Type(s) of the Card
# 	text = All of the text written on the card
# 	expansionSet = The set under which the card came out
# 	manaCost = The Converted Mana Cost of the card
# 	color = The color(s) of which the card is a part of
# 	power = Power of the card (if creature)
# 	toughness = Toughness of the card (if creature)
# 	art = Link to the image of the card
# 	rarity = Rarity of the card
# 	artist = Artist that made the card art
# 	"""

# 	__tablename__ = 'cards'

# 	#Relevant attributes for a card
# 	cardId = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(MED_LEN))
# 	mainType = db.Column(db.String(NAME_LEN))
# 	subtype = db.Column(db.String(MED_LEN), db.ForeignKey('subtypes.name'))
# 	text = db.Column(db.String(TEXT_LEN), nullable=True)
# 	expansionSet = db.Column(db.String(STG_LEN), db.ForeignKey('sets.code'))
# 	manaCost = db.Column(db.Integer, nullable=True)
# 	color = db.Column(db.String(SHORT_LEN), nullable=True)
# 	power = db.Column(db.Integer, nullable=True)
# 	toughness = db.Column(db.Integer, nullable=True)
# 	art = db.Column(db.String(MED_LEN))
# 	rarity = db.Column(db.String(STG_LEN))
# 	artist = db.Column(db.String(MED_LEN), db.ForeignKey('artists.name'))

# 	def __init__(self, cardId, name, mainType, subType, text, expansionSet,
# 				 manaCost, color, power, toughness, art, rarity, artist):
# 		self.cardId = cardId
# 		self.name = name
# 		self.mainType = mainType
# 		self.subType = subType
# 		self.text = text
# 		self.expansionSet = expansionSet
# 		self.manaCost = manaCost
# 		self.color = color
# 		self.power = power
# 		self.toughness = toughness
# 		self.art = art
# 		self.rarity = rarity
# 		self.artist = artist

# 	def __repr__(self):
# 		return '<Card %r>' % self.name

# class Set(db.Model):
# 	"""
# 	Information regarding card sets (A.K.A.: expansions)

# 	code = ID by which expansions can be identified
# 	name = Name of the expansions
# 	rDate = Release Date of the expansions
# 	block = Block that the expansion belongs to
# 	cards = Cards from this expansion
# 	subTypes = All subtypes in the expansion
# 	numCards = Number of cards that came out in the expansion
# 	symbol = Symbol used to identify the expansion on cards
# 	artists = Artists that made cards for this expansion
# 	"""

# 	__tablename__ = 'sets'

# 	code = db.Column(db.String(STG_LEN), primary_key=True)
# 	name = db.Column(db.String(MED_LEN))
# 	rDate = db.Column(db.String(NAME_LEN))
# 	block = db.Column(db.String(NAME_LEN), nullable=True)
# 	cards = db.relationship('Card', backref='set', lazy='dynamic')
# 	numCards = db.Column(db.Integer)
# 	symbol = db.Column(db.String(MED_LEN)) #link

# 	def __init__(self, code, name, rDate, block, cards, numCards,
# 				 symbol):
# 		self.code = code
# 		self.name = name
# 		self.rDate = rDate
# 		self.block = block
# 		self.cards = cards
# 		self.numCards = numCards
# 		self.symbol = symbol

# 	def __repr__(self):
# 		return '<Set %r>' % self.name

# class Artist(db.Model):
# 	"""
# 	Information regarding artists of MtG cards

# 	artistId = ID for artist
# 	name = Name of artist
# 	numCards = Number of cards this artist has worked on
# 	numSets = Number of Sets this artist has worked on
# 	cards = Cards that this artist has worked on
# 	sets = Sets that this artist has worked on
# 	"""

# 	__tablename__ = 'artists'

# 	#Possibility of repeated names
# 	artistId = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(MED_LEN))
# 	numCards = db.Column(db.Integer)
# 	numSets = db.Column(db.Integer)
# 	cards = db.relationship('Card', backref='artistboi', lazy='dynamic')

# 	def __init__(self, artistId, name, numCards, numSets, cards):
# 		self.artistId = artistId
# 		self.name = name
# 		self.numCards = numCards
# 		self.numSets = numSets
# 		self.cards = cards

# 	def __repr__(self):
# 		return '<Artist %r>' % self.name

# class Subtype(db.Model):
# 	"""
# 	Information regarding types

# 	name = Name of the subtype
# 	numCards = Number of existing cards of this subtype
# 	exCard = Image of a card of this subtype, to represent the subtype
# 	cards = cards that are of this subtype
# 	sets = Sets that contain cards of this subtype
# 	"""

# 	__tablename__ = 'subtypes'

# 	name = db.Column(db.String(MED_LEN), primary_key=True)
# 	numCards = db.Column(db.Integer)
# 	cards = db.relationship('Card', backref='scard', lazy='dynamic') 

# 	def __init__(self, name, numCards, cards):
# 		self.name = name
# 		self.numCards = numCards
# 		self.cards = cards

# 	def __repr__(self):
# 		return '<Subtype %r>' % self.name
