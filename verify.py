import os,json

sums = [i for i in [file for file in os.listdir(f"fillers/") if file.endswith('.json')] if str(json.load(open(f'fillers/{i}'))["total-episodes"]) and str(json.load(open(f'fillers/{i}'))["total-episodes"])!=len(list(json.load(open(f'fillers/{i}'))["episodes"]))]
print(sums)