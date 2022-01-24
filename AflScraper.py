import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://www.animefillerlist.com"
page = requests.get(url+"/shows")

soup = BeautifulSoup(page.content, "html.parser")
results = soup.select("#ShowList > .Group > ul > li > a")

links = {}

for i in results:
    links[re.search(".+(?=\()|.+",i.text)[0].removesuffix(" ")] = url+i.attrs["href"]

with open("fillers/links.json", "w") as fp:
    json.dump(links , fp, indent = 4) 