##########################
# Test script to check for event targets that are used but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from .imports.file_functions import open_text_file
import logging


def test_check_missing_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        if 'event_target:' in text_file:
            pattern_matches = re.findall('event_target:\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[13:].strip()
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - count the number of flag occurrences
    logging.debug(f'{len(event_targets)} used event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_targets = [i for i in event_targets.keys() if event_targets[i] == 0]

        if 'save_global_event_target_as =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'save_global_event_target_as = {target}')
        if 'save_event_target_as =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'save_event_target_as = {target}')

# Part 3 - throw the error if flag is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    if results != []:
        logging.warning("Following event targets are used but never set:")
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        raise AssertionError("Missing event targets were encountered! Check console output")