##########################
# Script to count tags
# By Pelmen, https://github.com/Pelmen323
##########################
import glob


def test_check_tags(test_runner: object):
    # filepath = filepath = f'{test_runner.full_path_to_mod}history\\countries\\'
    # filepath = 'C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\history\\countries\\'
    # filepath = 'C:\\SteamLibrary\\steamapps\\workshop\\content\\394360\\1826643372\\history\\countries\\'
    filepath = 'C:\\SteamLibrary\\steamapps\\workshop\\content\\394360\\2438003901\\history\\countries\\'
    counter = 0
# Part 1 - get the dict of oob usages in files
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        counter += 1

    print(counter)
