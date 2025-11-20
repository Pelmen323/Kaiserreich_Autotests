##########################
# Test script to check for states that are used but they not exist
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re


filepath_to_states = 'C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\history\\states'
results = {}

for filename in glob.iglob(filepath_to_states + '**/*.txt', recursive=True):
    with open(filename, 'r') as t:
        text_file = t.read()
        print(filename)
        if 'steel =' in text_file:
            coal_value = re.findall(r"steel\s*=\s*(\d+)", text_file)[0]
            name = os.path.basename(filename)[:-4]
            results[name] = coal_value

for i in results:
    print(f'{i}|{results[i]}')
