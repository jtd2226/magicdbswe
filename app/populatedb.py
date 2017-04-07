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

# ------
# SETS
# ------
print("starting sets")
with open('setCache.json') as sc:
    sets = json.load(sc)["allsets"]

for iset in sets:

	set_subTypes = list()
	for stype in iset["subTypes"]:
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

for artist in artists:

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
		card_subTypes.append(subCache[stype])

	if len(card_subTypes) == 0:
		card_subTypes = [subCache["none"]]

	temp = MCard(card["cardID"], card["name"], card["mainType"], card_subTypes, card["text"], card["expansionSet"], card["manaCost"], ", ".join(card["color"]), card["power"], card["toughness"], card["art"], card["rarity"], card["artist"])
	db.session.add(temp)
	db.session.commit()


