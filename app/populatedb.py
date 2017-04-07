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

stypeCount = 0

for stype in subtypes:
	stypeCount = stypeCount + 1
	print(str(stypeCount) + " subtype(s) added")

	temp = MSubtype(stype["name"], stype["numCards"])
	subCache[stype["name"]] = temp
	db.session.add(temp)
	db.session.commit()

# ------
# SETS
# ------
print("starting sets")
with open('setCache.json') as sc:
    sets = json.load(sc)["allsets"]

setCount = 0
for iset in sets:
	setCount = setCount + 1
	print(str(setCount) + " set(s) added")

	set_subTypes = list()
	for stype in iset["subTypes"]:
		if stype in subCache:
			set_subTypes.append(subCache[stype])

	if len(set_subTypes) == 0:
		set_subTypes = [subCache["none"]]

	temp = MSet(iset["code"], iset["name"], iset["rDate"], iset["block"], iset["numCards"], iset["symbol"], set_subTypes)
	setCache[iset["code"]] = temp

	db.session.add(temp)
	db.session.commit()

# ---------
# ARTISTS
# ---------
print("starting artists")
with open('artistCache.json') as ac:
    artists = json.load(ac)

artistCount = 0
for artist in artists:
	artistCount = artistCount + 1
	print(str(artistCount) + " artist(s) added")

	artists_sets = list()
	for a in artists[artist]["sets"]:
		artists_sets.append(setCache[a])

	if len(artists_sets) == 0:
		artists_sets = [setCache["none"]]

	temp = MArtist(artist, artists[artist]["numCards"], artists[artist]["numSets"], artists_sets)
	artCache[artist] = temp

	db.session.add(temp)
	db.session.commit()


# -------
# CARDS
# -------
print ("starting cards")
with open('cardCache.json') as cc:
    cards = json.load(cc)["allcards"]

cardCount = 0
for card in cards:
	cardCount = cardCount + 1
	print(str(cardCount) + " card(s) added")
	card_subTypes = list()
	for stype in card["subtype"]:
		if stype in subCache:
			card_subTypes.append(subCache[stype])

	if len(card_subTypes) == 0:
		card_subTypes = [subCache["none"]]

	temp = MCard(card["cardID"], card["name"], card["mainType"], card_subTypes, card["text"], card["expansionSet"], card["manaCost"], ", ".join(card["color"]), card["power"], card["toughness"], card["art"], card["rarity"], card["artist"])
	
	#if db.session.query(MCard).filter_by(cardId=card["cardID"]).first() is None:
	db.session.add(temp)
	db.session.commit()


