import requests, os , json
from bs4 import BeautifulSoup
from os.path import exists

url = "https://www.animefillerlist.com"

query = """
query ($search: String) { 
  Media (search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
    }
    episodes
  }
}
"""

def variable(name):return {'search': name}

def executeQuery(query,variables):
    headers = {"Content-Type": "application/json","Accept": "application/json"}
    return json.loads(requests.post("https://graphql.anilist.co/",headers=headers,json={"query":query,"variables":variables}).content)


# print (executeQuery(query=query,variables=variable("cowboy")))


with open("links.json") as f:
#f = open('links.json')
  links = json.load(f)
 
for i in links.keys():
  anilistData = executeQuery(query=query,variables=variable(i))["data"]["Media"]
  if exists("fillers/"+str(anilistData["idMal"])+".json"):continue
  data = {
    "mal-id": anilistData["idMal"],
    "anilist-id": anilistData["id"],
    "anilist-name_en": anilistData["title"]["english"],
    "anilist-name_jp": anilistData["title"]["romaji"],
    "total-episodes": anilistData["episodes"],
    "afl-name":i,
    "afl-link":links[i],
    "fillers_episodes":[],
    "episodes":[]
  }
  print(f'{anilistData["id"]} : {anilistData["title"]["romaji"]}')
  linkSoup = BeautifulSoup(requests.get(links[i]).content, "html.parser")
  print(links[i])
  for i in linkSoup.select(".EpisodeList > tbody > tr "):
    episode = {
      "title": i.select_one("td.Title").text,
      "number": i.select_one("td.Number").text,
      "filler": i.select_one("td.Type").text, 
      "filler-bool": False, 
    }
    if "canon" not in episode["filler"].lower():episode["filler-bool"] = True and data["fillers_episodes"].append(episode["number"])
    # episode = {}
    # pageSoup = BeautifulSoup(requests.get(url+i.attrs["href"]).content, "html.parser")
    # node = pageSoup.select_one(".node")
    # fields = node.select(".content > .field")
    # episode["title"] = node.select_one("h1").text
    # for i in fields:
    #     label = i.select_one(".field-label")
    #     if(label!=None):
    #         san_label = label.text.strip()
    #         value = i.select_one(".field-items").text

    #         match san_label:
    #             case "Episode Number:" : 
    #               episode["number"] = value
    #             case "Type:" :
    #               episode["filler"] = value
    #               episode["filler_bool"] = False
    #               if "canon" not in value.lower():
    #                 episode["filler_bool"] = True
    #                 data["fillers_episodes"].append(episode["number"])
    #     else:
    #         episode["description"] = i.select_one(".field-items > .field-item").text
    print(episode)
    data["episodes"].append(episode)
  with open(f'fillers/{anilistData["idMal"]}.json', "w") as fp:json.dump(data , fp, indent = 4) 
