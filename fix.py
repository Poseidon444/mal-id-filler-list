import json

diff = 11
fileName = "72.json"

f = open(fileName)
data = json.load(f)

a = []
for i in list(data["fillers_episodes"]):
    a.append(str(int(i)-diff))
data["fillers_episodes"] = a
b = []
for i in list(data["episodes"]):
    i["number"] = str(int(i["number"])-diff)
    b.append(i)

data["episodes"] = b

with open(fileName, "w") as fp:
    json.dump(data , fp, indent = 4) 