import json
from mtgsdk import Card, Set, Subtype

with open('logo.json') as surl:
    surldict = json.load(surl)

sets = Set.all()

print("{")
print("\"allsets\":	[")

for iset in sets:
	cardSetList = Card.where(set=iset.code) \
 					  .all()

	print("{")

	set_code = "none"
	if iset.code is not None:
		set_code = iset.code
	print("\"code\":" + "\"" + set_code + "\",")

	set_name = "none"
	if iset.name is not None:
		set_name = iset.name
	print("\"name\":" + "\"" + set_name + "\",")

	set_rDate = "none"
	if iset.release_date is not None:
		set_rDate = iset.release_date
	print("\"rDate\":" + "\"" + set_rDate + "\",")

	set_block = "none"
	if iset.block is not None:
		set_block = iset.block
	print("\"block\":" + "\"" + set_block + "\",")

	print("\"numCards\":" + str(int(len(cardSetList))) + ",")

	print("\"symbol\":" + "\"" + surldict[iset.code] + "\",")

	set_subTypes = ["none"]
	for card in cardSetList: 
		slist = list()
		if card.subtypes is not None:
			for stype in card.subtypes:
				slist.append(stype)
		set_subTypes = slist
	set_subTypes = json.dumps(set_subTypes)
	print("			\"subTypes\":" + set_subTypes)

	print("},")

print("REMEMBER TO DELETE TRAILING COMMA")
print("	]")
print("}")