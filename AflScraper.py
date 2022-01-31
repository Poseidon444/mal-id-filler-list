import requests, json, re
from bs4 import BeautifulSoup

url = "https://www.animefillerlist.com"
page = requests.get(f"{url}/shows")

soup = BeautifulSoup(page.content, "html.parser").select("#ShowList > .Group > ul > li > a")

links = {re.search(".+(?=\()|.+",i.text)[0].removesuffix(" "):url+i.attrs["href"] for i in soup}

with open("links.json", "w") as fp:json.dump(links , fp, indent = 4) 