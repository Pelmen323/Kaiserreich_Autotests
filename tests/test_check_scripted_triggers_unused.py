##########################
# Test script to check if there are scripted triggers that are not used via "xxx = yes" or "xxx = no"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from .imports.file_functions import open_text_file
import logging


def test_check_scripted_triggers_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_effects = f'{test_runner.full_path_to_mod}common\\scripted_triggers\\'
    dict_with_scripted_triggers = {}
    paths = {}
    # 1. Get the dict of all scripted effects
    for filename in glob.iglob(filepath_to_effects + '**/*.txt', recursive=True):
        if 'diplomacy_scripted_triggers' in filename:                   # These triggers are NOT used directly
            continue
        if 'diplo_action_valid_triggers' in filename:
            continue
        if '00_resistance' in filename:
            continue
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            pattern_matches = re.findall('^[a-zA-Z0-9_\\.]* = \\{', current_line)
            if len(pattern_matches) > 0:
                match = pattern_matches[0][:-4].strip()
                dict_with_scripted_triggers[match] = 0
                paths[match] = os.path.basename(filename)

    # 2. Find if scripted effects are used:
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_triggers = [i for i in dict_with_scripted_triggers.keys() if dict_with_scripted_triggers[i] == 0]
        if ' = yes' in text_file or ' = no' in text_file:
            for key in not_encountered_triggers:
                if f'{key} = yes' in text_file:
                    dict_with_scripted_triggers[key] += 1
                if f'{key} = no' in text_file:
                    dict_with_scripted_triggers[key] += 1

    results = [i for i in dict_with_scripted_triggers.keys() if dict_with_scripted_triggers[i] == 0]
    if results != []:
        logging.warning("Unused scripted triggers found:")
        for i in results:
            logging.error(f"- [ ] {i} - '{paths[i]}'")
        logging.warning(f'{len(results)} unused scripted triggers found.')
        raise AssertionError("Unused scripted triggers found! Check console output")
