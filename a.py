import os,json

path_to_json = 'fillers/'

for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
  with open(path_to_json + file_name) as json_file:
    data = json.load(json_file)
    if(str(data["total-episodes"])!=list(data["episodes"])[-1]["number"]):
        print(file_name)