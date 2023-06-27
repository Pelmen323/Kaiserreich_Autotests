import glob
import os

filepath = "input\\"

for filename in glob.iglob(filepath + '**/*.dds', recursive=True):
    if "LIT_" in filename:
        os.rename(filename, filename.replace("LIT_", "EE_"))
    # os.rename(filename, f'{filename[:-4]}_alt.png')
