import models
import json
import urllib.request

purl = "http://ggnoswe.me/api/platforms/"
surl = "http://ggnoswe.me/api/studios/"
gurl = "http://ggnoswe.me/api/games/"

platforms = [
  {
    "id": 41, 
    "name": "Wii U"
  },    
  {
    "id": 37, 
    "name": "Nintendo 3DS"
  }, 
  {
    "id": 48, 
    "name": "PlayStation 4"
  }, 
  {
    "id": 49, 
    "name": "Xbox One"
  }, 
  {
    "id": 130, 
    "name": "Nintendo Switch"
  },
  {
    "id": 12, 
    "name": "Xbox 360"
  }, 
  {
    "id": 9, 
    "name": "PlayStation 3"
  }
]

root = {"name": "flare",
 		"description": "flare",
 		"children": []}

count = 0
for p in platforms:
  cp = json.loads(urllib.request.urlopen(purl + str(p["id"])).read().decode())
  d = {}
  d["name"] = p["name"]
  d["description"] = cp["summary"]
  d["children"] = []

  for s in cp["studios"] :
    cs = json.loads(urllib.request.urlopen(surl + str(s)).read().decode())
    d["children"].append({"name": cs["name"],"description": cs["description"], "size": len(cs["games"])})
    print(count)
    count = count + 1

  root["children"].append(d)

with open('templates/flare.json', 'w') as outfile:
    json.dump(root, outfile)