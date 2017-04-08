import json
from mtgsdk import Card, Set, Subtype

with open('cardCache.json') as surl:
    carddict = json.load(surl)

artistdict = dict()

for card in carddict["allcards"]:

	if card["artist"] not in artistdict:
		artistdict[card["artist"]] = dict()
		artistdict[card["artist"]]["numCards"] = 1
		artistdict[card["artist"]]["sets"] = [card["expansionSet"]]
		artistdict[card["artist"]]["numSets"] = len(artistdict[card["artist"]]["sets"])

	else :
		artistdict[card["artist"]]["numCards"] = artistdict[card["artist"]]["numCards"] + 1
		if card["expansionSet"] not in artistdict[card["artist"]]["sets"]:
			artistdict[card["artist"]]["sets"].append(card["expansionSet"])
			artistdict[card["artist"]]["numSets"] = len(artistdict[card["artist"]]["sets"])

print (json.dumps(artistdict))



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

	