import models

from mtgsdk import Card, Set, Subtype
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, MCard, MSet, MArtist, MSubtype


#----------
# SUBTYPES
#----------
subtypes = Subtype.all() 

for stype in subtypes:
	cardSetList = Card.where(subtypes=stype) \
 					  .all()
	temp = MSubtype(stype, len(cardSetList))
	db.session.add(temp)
	db.session.commit()



#------
# SETS
#------

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

# 	set_symbol = str()


#-------
# CARDS
#-------

# cards = Card.all()

# for card in cards:

# 	print("------------------------")
	
# 	card_Id = card.multiverse_id
# 	print(card_Id)

# 	card_name = card.name
# 	print(card_name)

# 	card_mainType = card.type
# 	print(card_mainType)

# 	card_subtype = str(card.subtypes)		#todo: relationship between subtypes and cards
# 	print(card_subtype)

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

# 	card_artist = card.artist   
# 	print(card_artist)	

#---------
# ARTISTS
#---------







#json stuff just in case 
# with open('../AllSets.json') as file:
# 	Sets = json.load(file)

# for key in Sets:
	
# 	for card in Sets[key]['cards']: