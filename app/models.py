#
# A Database for Magic the Gathering Cards
#
# pylint:disable=invalid-name,line-too-long,no-member,too-few-public-methods,locally-disabled
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
STG_LEN = 12
NAME_LEN = 32
SHORT_LEN = 128
MED_LEN = 256
TEXT_LEN = 1024


class Card(db.Model):

	"""
	Information regarding specific cards

	cardId = Unique ID to identify a card
	name = Name of the card
	mainType = Primary Type of the Card
	subType = Secondary Type of the Card
	text = All of the text written on the card
	expansionSet = The set under which the card came out
	manaCost = The Converted Mana Cost of the card
	color = The color(s) of which the card is a part of
	pt = Power and Toughness of the card
	art = Link to the image of the card
	rarity = Rarity of the card
	artist = Artist that made the card art
	"""

	__tablename__ = 'Cards'

	#Relevant attributes for a card
	cardId = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(MED_LEN))
	mainType = db.Column(db.String(NAME_LEN))
	subType = db.Column(db.String(NAME_LEN), db.ForeignKey('Subtypes.name'), nullable=True)
	text = db.Column(db.String(TEXT_LEN), nullable=True)
	expansionSet = db.Column(db.String(MED_LEN), db.ForeignKey('Sets.code'))
	manaCost = db.Column(db.Integer, nullable=True)
	color = db.Column(db.String(SHORT_LEN), nullable=True)
	pt = db.Column(db.String(STG_LEN), nullable=True)
	art = db.Column(db.String(MED_LEN))
	rarity = db.Column(db.String(STG_LEN))
	artist = db.Column(db.String(MED_LEN), db.ForeignKey('Artists.name'))

	def __init__(self, cardId, name, mainType, subType, text, expansionSet,
				 manaCost, color, pt, art, rarity, artist):
		self.cardId = cardId
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

	code = ID by which expansions can be identified
	name = Name of the expansions
	rDate = Release Date of the expansions
	block = Block that the expansion belongs to
	numCards = Number of cards that came out in the expansion
	symbol = Symbol used to identify the expansion on cards
	"""

	__tablename__ = 'Sets'

	"""
	Cards and Artists are related to Sets, but shall use a relation to a join table
	"""

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

	artistId = 
	"""

	__tablename__ = 'Artists'

	#Possibility of repeated names
	artistId = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(MED_LEN))
	numCards = db.Column(db.Integer)
	numSets = db.Column(db.Integer)
	cards = db.Column(db.String(MED_LEN)) #link or something new to write
	#sets = db.Column(db.String(MED_LEN))

	def __init__(self, artistId, name, numCards, numSets, cards, sets):
		self.artistId = artistId
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

	__tablename__ = 'SubTypes'

	name = db.Column(db.String(MED_LEN), primary_key=True)
	numCards = db.Column(db.Integer)
	exCard = db.Column(db.String(MED_LEN), db.ForeignKey('Cards.cardId'))
	#cards = db.Column(db.String(MED_LEN)) #This is a link

	#Set this subtype most appears in
	mostPopularSet = db.Column(db.String(NAME_LEN), db.ForeignKey('Sets.code'))

	def __init__(self, name, numCards, cards, exCard, mostPopularSet):
		self.name = name
		self.numCards = numCards
		#self.cards = cards
		self.exCard = exCard
		self.mostPopularSet = mostPopularSet

	def __repr__(self):
		return '<Subtype %r>' % self.name