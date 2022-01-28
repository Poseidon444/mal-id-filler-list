import json

diff,fileName = 11,"72.json"

f = open(fileName)
data = json.load(f)

data["fillers_episodes"] = [str(int(i)-diff) for i in data["fillers_episodes"]]


b = []
for i in list(data["episodes"]):i["number"] = str(int(i["number"])-diff) and b.append(i)


data["episodes"] = b

with open(fileName, "w") as fp:json.dump(data , fp, indent = 4) 