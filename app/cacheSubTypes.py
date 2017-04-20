import json
from mtgsdk import Card, Set, Subtype

subtypes = Subtype.all() 

print("{")
print("\"subtypes\":	[")

with open('setCache.json') as sc:
	sets = json.load(sc)["allsets"]

for stype in subtypes:
	cardSetList = Card.where(subtypes=stype) \
 					  .all()

	print("{")

	print("\"name\":" + "\"" + stype + "\",")

	print("\"numCards\":" + str(int(len(cardSetList))) + ",")

	numSets = 0
	
	for iset in sets:
		if stype in iset["subTypes"]:
			numSets = numSets + 1
	
	print("\"numSets\":" + str(numSets))

	print("},")

print("REMEMBER TO DELETE TRAILING COMMA")
print("]")
print("}")