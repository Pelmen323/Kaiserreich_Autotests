import glob
import os


INPUT_FOLDER = 'C:\\Repos\\Kaiserreich_Tests\\input_images\\'
for filename in glob.iglob(INPUT_FOLDER + "**/*.png", recursive=True):
    os.rename(filename, filename.replace("CAN_", "ENG_"))

