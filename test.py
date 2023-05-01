import json

# Replace 'file_name.json' with the path to your JSON file
file_path = 'intermediate.json'

with open(file_path, 'r') as file:
    data = json.load(file)

print(data)