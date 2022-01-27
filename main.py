import requests, json, re, os, time
from bs4 import BeautifulSoup
from os.path import exists
if exists('links.json'):pass
else:
    url = "https://www.animefillerlist.com"
    soup = BeautifulSoup(requests.get(f"{url}/shows").content, "html.parser").select("#ShowList > .Group > ul > li > a")
    links = {re.search(".+(?=\()|.+",i.text)[0].removesuffix(" "):url+i.attrs["href"] for i in soup}
    with open("links.json", "w") as f:json.dump(links , f, indent = 4)

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
    nextAiringEpisode{
      episode
    }
  }
}
"""

def variable(name):return {'search': name}

def executeQuery(query,variables):return json.loads(requests.post("https://graphql.anilist.co/",headers={"Content-Type": "application/json","Accept": "application/json"},json={"query":query,"variables":variables}).content)


# print (executeQuery(query=query,variables=variable("cowboy")))

l = []
with open("links.json") as f:links = json.load(f)
 
for i in links.keys():

    try:
        time.sleep(0.1)
        print(f"working:{i}")
        anilistData = executeQuery(query=query,variables=variable(i))['data']['Media']
        if exists("fillers"):pass
        else:os.mkdir("fillers")
        if exists("fillers/"+str(anilistData["idMal"])+".json") : continue
        data = {
        "mal-id": anilistData["idMal"],
        "anilist-id": anilistData["id"],
        "anilist-name_en": anilistData["title"]["english"],
        "anilist-name_jp": anilistData["title"]["romaji"],
        "afl-name":i,
        "afl-link":links[i],
        "fillers_episodes":[],
        "episodes":[]
    }   
        if anilistData['nextAiringEpisode'] is None:
          data['nextAiringEpisode'] = "Unknown"
          data['total-episodes'] = anilistData['episodes']
        elif anilistData['nextAiringEpisode']['episode']:
          data["total-episodes"] = [int(anilistData['nextAiringEpisode']['episode'] - 1)]
          data['nextAiringEpisode'] = anilistData['nextAiringEpisode']['episode']
        elif anilistData['total-episodes'] is None:data['total-episodes'] = "Unknown"
        else:anilistData['total-episodes'] = data['total-episodes']

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
            #if "canon" not in episode["filler"].lower():
            #  episode["filler-bool"] = True
            #  data["fillers_episodes"].append(episode["number"])
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
            #                 episode["filler_bool"] = 
            # True
            #                 data["fillers_episodes"].append(episode["number"])
            #     else:
            #         episode["description"] = i.select_one(".field-items > .field-item").text
            print(episode)
            data["episodes"].append(episode)
        data['fillers_episodes'] = [i['number'] for i in data['episodes'] if not i['filler'].lower().__contains__("canon")]
        with open(f'fillers/{anilistData["idMal"]}.json', "w") as fp:json.dump(data , fp, indent = 4) 
    except:
        print("err",i)
        #l.append(i)
        #print(i)
#for i in l:del links[i]
#print(l)