import json
from mtgsdk import Card, Set, Subtype

cards = Card.all()

print("{")
print("\"allcards\":[")

for card in cards:

	print("		{")
	
	card_Id = card.id
	print("			\"cardID\":" + "\"" + card_Id + "\",")

	card_name = "none"
	if card.name is not None:
		card_name = card.name
	print("			\"name\":" + "\"" + card_name + "\",")

	card_mainType = "none"
	if card.type is not None:
		card_mainType = card.type
	print("			\"mainType\":" + "\"" + card_mainType + "\",")

	slist = ["none"]
	if(card.subtypes is not None):
		slist = list()
		for stype in card.subtypes:
			slist.append(stype)
	card_subtype = json.dumps(slist)
	print("			\"subtype\":" + card_subtype + ",")
	
	card_text = "\"none\""
	if card.text is not None:
		card_text = json.dumps(card.text)
	print("			\"text\":" + card_text + ",")

	card_expansionSet = "none"
	if card.set is not None:
		card_expansionSet = card.set  
	print("			\"expansionSet\":" + "\"" + card_expansionSet + "\",")

	card_manaCost = "null"
	if card.cmc is not None:
		card_manaCost = card.cmc
	print("			\"manaCost\":" + str(card_manaCost) + ",")

	card_color = "[\"none\"]"
	if card.colors is not None:
		card_color = json.dumps(card.colors)	
	print("			\"color\":" + card_color + ",")

	card_power = "none"
	if card.power is not None:
		card_power =  card.power
	print("			\"power\":" + "\"" + card_power + "\",")

	card_toughness = "none"
	if card.toughness is not None:
		card_toughness = card.toughness
	print("			\"toughness\":" + "\"" + card_toughness + "\",")

	card_art = "none"
	if card.image_url is not None:
		card_art = card.image_url
	print("			\"art\":" + "\"" + card_art + "\",")

	card_rarity = "none"
	if card.rarity is not None:
		card_rarity = card.rarity
	print("			\"rarity\":" + "\"" + card_rarity + "\"")

	print("		},")

print("REMEMBER TO DELETE TRAILING COMMA")
print("	]")
print("}")