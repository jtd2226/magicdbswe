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
	print("\"code\":" + "\"" + set_code + "\"")

	set_name = "none"
	if iset.name is not None:
		set_name = iset.name
	print("\"name\":" + "\"" + set_name + "\"")

	set_rDate = "none"
	if iset.release_date is not None:
		set_rDate = iset.release_date
	print("\"rDate\":" + "\"" + set_rDate + "\"")

	set_block = "none"
	if iset.block is not None:
		set_block = iset.block
	print("\"block\":" + "\"" + set_block + "\"")

	print("\"numCards\":" + str(int(len(cardSetList))))

	print("\"symbol\":" + "\"" + surldict[iset.code] + "\"")

	set_subTypes = [subCache["none"]]

	print("},")

print("REMEMBER TO DELETE TRAILING COMMA")
print("	]")
print("}")

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

	