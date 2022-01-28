import os, json

for z in os.listdir("fillers"):
    with open(f'fillers/{z}') as f:data = json.load(f)
    for i in data['episodes']:
        print(i['filler-bool'])
        if 'canon' not in i['filler'].lower():i["filler-bool"] = True
        elif 'canon' in i['filler'].lower():i["filler-bool"] = False
        print(f"changed:{i['filler-bool']}")

    with open(f'fillers/{z}', "w") as fp:json.dump(data , fp, indent = 4) 

