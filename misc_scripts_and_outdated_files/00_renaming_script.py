import glob
import os

filepath = "input\\"

for filename in glob.iglob(filepath + '**/*.png', recursive=True):
    if "main_tank" in filename:
        os.rename(filename, filename.replace("main", "medium"))
    # os.rename(filename, f'{filename[:-4]}_alt.png')
