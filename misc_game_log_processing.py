import glob
import re
from collections import Counter

"""
Game log processing script
"""

INPUT_FOLDER = 'C:\\Repos\\Kaiserreich_Tests\\input_images\\'
pattern = re.compile(r': ([^,\n]+)')
container = []
for filename in glob.iglob(INPUT_FOLDER + "**/*.log", recursive=True):
    print("1111")
    with open(filename, 'r', encoding='utf-8') as file:
        text_file = file.read()

    pattern_matches = pattern.findall(text_file)
    for match in pattern_matches:
        if len(match) < 8 or "LBA" in match:
            continue
        container.append(match)

counts = Counter(container)
results = {key: value for key, value in counts.items() if value > 200}

sorted_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
for key, value in sorted_dict.items():
    print(f'{key} - {value}')
