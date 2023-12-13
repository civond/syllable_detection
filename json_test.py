import json
import toml
import os

JS = open('config.json');
data = json.load(JS)
#print(data)
# Iterating through the json
# list
#write_dir = data['write_directory']
#if not os.path.exists(write_dir):
#    os.makedirs(write_dir)

#with open('options.toml', 'r') as f:
#    config = toml.load(f)
with open('config.toml', 'r') as f:
    config = toml.load(f)

write_dir = config["Directories"]['write_directory']
print(os.path.exists(write_dir))


print(config["Main"])
#print(config["Mask_Generation"]["time_short"])