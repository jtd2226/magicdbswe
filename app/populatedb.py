import models
import json

#from mtgsdk import Card, Set, Subtype
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, MCard, MSet, MArtist, MSubtype

# ----------
#  SUBTYPES
# ----------

db.session.commit()
db.drop_all()
db.create_all()
subCache = dict()
artCache = dict()
setCache = dict()


with open('stypeCache.json') as scache:
    subtypes = json.load(scache)["subtypes"]

subCache["none"] = MSubtype("none", 0)

for stype in subtypes:
	temp = MSubtype(stype["name"], stype["numCards"])
	subCache[stype["name"]] = temp
	db.session.add(temp)
	db.session.commit()

# # ------
# # SETS
# # ------
# with open('logo.json') as surl:
#     surldict = json.load(surl)

# sets = Set.all()

# for iset in sets:

# 	print("------------------------")

# 	set_code = iset.code
# 	print(set_code)

# 	set_name = iset.name
# 	print(set_name)

# 	set_rDate = iset.release_date
# 	print(set_rDate)

# 	set_block = iset.block
# 	print(set_block)

# 	cardSetList = Card.where(set=iset.code) \
# 					  .all()
	
# 	set_numCards = len(cardSetList)
# 	print(set_numCards)

# 	set_symbol = surldict[iset.code]
# 	print(set_symbol)

# 	set_subTypes = [subCache["none"]]

# 	temp = MSet(set_code, set_name, set_rDate, set_block, set_numCards, set_symbol, set_subTypes)

# 	db.session.add(temp)
# 	db.session.commit()

# # -------
# # CARDS
# # -------

# cards = Card.all()

# for card in cards:

# 	print("------------------------")
	
# 	card_Id = card.id
# 	print(card_Id)

# 	card_name = card.name
# 	print(card_name)

# 	card_mainType = card.type
# 	print(card_mainType)

# 	card_subtype = [subCache["none"]]
# 	if(card.subtypes is not None):
# 		slist = list()
# 		for stype in card.subtypes:
# 			slist.append(subCache[stype])
# 		card_subtype = slist
	
# 	card_text = card.text
# 	print(card_text)

# 	card_expansionSet = card.set  
# 	print(card_expansionSet)

# 	card_manaCost = card.cmc
# 	print(card_manaCost)

# 	card_color = str(card.colors)		#todo
# 	print(card_color)

# 	card_power =  card.power
# 	print(card_power)

# 	card_toughness = card.toughness
# 	print(card_toughness)

# 	card_art = card.image_url
# 	print(card_art)

# 	card_rarity = card.rarity
# 	print(card_rarity)


# # ---------
# # ARTISTS
# # ---------

# 	cardArtList = Card.where(artist=card.artist) \
#  					  .all()

#  	artist_sets = list()

# 	disArtCache = dict()
# 	for zcard in cardArtList:
#   		disArtCache[zcard.set] = 1

# 	if card.artist not in artCache:
# 		artCache[card.artist] = 1
# 		tempa = MArtist(card.artist, int(len(cardArtList)), len(disArtCache.keys()), artist_sets)
# 		db.session.add(tempa)
# 		db.session.commit()

# 	card_artist = card.artist
# 	print(card_artist)

# 	temp = MCard(card_Id, card_name, card_mainType, card_subtype, card_text, card_expansionSet, card_manaCost, card_color, card_power, card_toughness, card_art, card_rarity, card_artist)

# 	db.session.add(temp)
# 	db.session.commit()
