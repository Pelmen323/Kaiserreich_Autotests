##########################
# Test script to check if there are scripted effects that are not used via "xxx = yes"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from .imports.file_functions import open_text_file
import logging


def test_check_scripted_effects_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_effects = f'{test_runner.full_path_to_mod}common\\scripted_effects\\'
    dict_with_scripted_effects = {}
    paths = {}
    # 1. Get the dict of all scripted effects
    for filename in glob.iglob(filepath_to_effects + '**/*.txt', recursive=True):
        text_file = open_text_file(filename)

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            pattern_matches = re.findall('^[a-zA-Z0-9_\\.]* = \\{', current_line)
            if len(pattern_matches) > 0:
                match = pattern_matches[0][:-4].strip()
                dict_with_scripted_effects[match] = 0
                paths[match] = os.path.basename(filename)

    # 2. Find if scripted effects are used:
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = open_text_file(filename)

        not_encountered_effects = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0]
        if ' = yes' in text_file:
            for key in not_encountered_effects:
                if f'{key} = yes' in text_file:
                    dict_with_scripted_effects[key] += 1

    results = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0]
    if results != []:
        logging.warning("Unused scripted effects found!:")
        for i in results:
            logging.error(f"- [ ] {i} - '{paths[i]}'")
        logging.warning(f'{len(results)} unused scripted effects found.')
        raise AssertionError("Unused scripted effects found! Check console output")
