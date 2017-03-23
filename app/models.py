#
# A Database for Magic the Gathering Cards
#
# pylint:disable=invalid-name,line-too-long,no-member,too-few-public-methods,locally-disabled
from flask import Flask
from flask-sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

NAME_LEN = 32
MED_LEN = 256
SHORT_LEN = 128
TEXT_LEN = 1024
STG_LEN = 12

class Card(db.Model):

	"""
	Information regarding specific cards
	"""

	__tablename__ = 'Cards'

	#consider not making name a primary_key, use multiverseId
	#unless there are many sets per entry of a card
	multiID = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(MED_LEN))
	mainType = db.Column(db.String(NAME_LEN))
	subType = db.Column(db.String(NAME_LEN), db.ForeignKey('Subtypes.name'), nullable=True)
	text = db.Column(db.String(TEXT_LEN), nullable=True)
	expansionSet = db.Column(db.String(MED_LEN), db.ForeignKey('Sets.code'))
	manaCost = db.Column(db.Integer, nullable=True) #Wheel of Fate edgecase
	color = db.Column(db.String(SHORT_LEN), nullable=True)
	pt = db.Column(db.String(STG_LEN), nullable=True)
	art = db.Column(db.String(MED_LEN))
	rarity = db.Column(db.String(STG_LEN))
	artist = db.Column(db.String(MED_LEN), db.ForeignKey('Artists.name'))

	def __init__(self, multiID, name, mainType, subType, text, expansionSet,
				 manaCost, color, pt, art, rarity, artist):
		self.multiID = multiID
		self.name = name
		self.mainType = mainType
		self.subType = subType
		self.text = text
		self.expansionSet = expansionSet
		self.manaCost = manaCost
		self.color = color
		self.pt = pt
		self.art = art
		self.rarity = rarity
		self.artist = artist

	def __repr__(self):
		return '<Card %r>' % self.name

class Set(db.Model):
	"""
	Information regarding card sets (A.K.A.: expansions)
	"""

	__tablename__ = 'Sets'

	code = db.Column(db.String(STG_LEN), primary_key=True)
	name = db.Column(db.String(MED_LEN))
	rDate = db.Column(db.String(NAME_LEN))
	block = db.Column(db.String(NAME_LEN), nullable=True)
	#cards = db.Column(db.String(MED_LEN)) #link
	numCards = db.Column(db.Integer)
	symbol = db.Column(db.String(MED_LEN)) #link
	#artists = db.Column(db.String(NAME_LEN))

	def __init__(self, code, name, rDate, block, cards, numCards,
				 symbol, artists):
		self.code = code
		self.name = name
		self.rDate = rDate
		self.block = block
		#self.cards = cards
		self.numCards = numCards
		self.symbol = symbol
		#self.artists = artists

	def __repr__(self):
		return '<Set %r>' % self.name

class Artist(db.Model):
	"""
	Information regarding artists of MtG cards
	"""

	__tablename__ = 'Artists'

	#Possibility of repeated names
	iden = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(MED_LEN))
	numCards = db.Column(db.Integer)
	numSets = db.Column(db.Integer)
	cards = db.Column(db.String(MED_LEN)) #link or something new to write
	#sets = db.Column(db.String(MED_LEN))

	def __init__(self, iden, name, numCards, numSets, cards, sets):
		self.iden = iden
		self.name = name
		self.numCards = numCards
		self.numSets = numSets
		self.cards = cards
		#self.sets = sets

	def __repr__(self):
		return '<Artist %r>' % self.name

class SubType(db.Model):
	"""
	Information regarding types
	"""

	__table__ = 'SubTypes'

	name = db.Column(db.String(MED_LEN), primary_key=True)
	numCards = db.Column(db.Integer)
	exCard = db.Column(db.String(MED_LEN), db.ForeignKey('Cards.name'))
	#cards = db.Column(db.String(MED_LEN)) #This is a link

	#Set this subtype most appears in
	mostSet = db.Column(db.String(NAME_LEN), db.ForeignKey('Sets.name'))

	def __init__(self, name, numCards, cards, exCard, mostSet):
		self.name = name
		self.numCards = numCards
		#self.cards = cards
		self.exCard = exCard
		self.mostSet = mostSet

	def __repr__(self):
		return '<Subtype %r>' % self.name