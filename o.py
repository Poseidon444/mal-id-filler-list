import os, json

for i in os.listdir("fillers"):
    with open(f'fillers/{i}') as f:data = json.load(f)
    for i in data['episodes']:
        print(i['filler-bool'])
        if "canon" in i['filler'].lower():i['filler-bool'] =  False
        else:i['filler-bool'] = True
        print(f"changed:{i['filler-bool']}")