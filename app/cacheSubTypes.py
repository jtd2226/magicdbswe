from mtgsdk import Card, Set, Subtype

subtypes = Subtype.all() 

print("{")
print("[")

for stype in subtypes:
	cardSetList = Card.where(subtypes=stype) \
 					  .all()

	print("{")

	print("\"name\":" + "\"" + stype + "\",")

	print("\"numCards\":" + str(int(len(cardSetList))))

	print("},")

print("REMEMBER TO DELETE TRAILING COMMA")
print("]")
print("}")