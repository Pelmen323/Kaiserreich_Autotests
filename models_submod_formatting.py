import glob
import re
from collections import Counter

"""
Game log processing script
"""

INPUT_FOLDER = 'C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Models Dev Build\\gfx\\entities\\z_units_KR_GER.asset'

with open(INPUT_FOLDER, 'r', encoding='utf-8') as file:
    text_file = file.read()
    replacement_dict = {}
    entity_match = re.findall(r'entity = \{[^\}]+\}', text_file, flags=re.DOTALL | re.MULTILINE)
    if len(entity_match) > 0:
        for i in entity_match:
            if 'attach' in i:
                continue
            try:
                name_match = re.findall(r'name = ".*?"', i)[0]
                pdxmesh_match = re.findall(r'pdxmesh = ".*?"', i)[0]
                clone_match = re.findall(r'clone = ".*?"', i)[0]
            except Exception:
                continue

            assembled_replacement = f"entity = {{ {name_match:<55}{clone_match:<50}{pdxmesh_match} }}"
            replacement_dict[i] = assembled_replacement

text_file_new = text_file
for i in replacement_dict:
    text_file_new = text_file_new.replace(i, replacement_dict[i])

with open(INPUT_FOLDER, 'w', encoding='utf-8') as text_file_write:
    text_file_write.write(text_file_new)
