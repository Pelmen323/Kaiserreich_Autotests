##########################
# Test script to check for event targets that are not used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file
import logging


def test_check_unused_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        if 'save_global_event_target_as =' in text_file:
            event_targets_in_file = re.findall('save_global_event_target_as = \\w*\\b', text_file)
            if len(event_targets_in_file) > 0:
                for target in event_targets_in_file:
                    target = target[29:].strip()
                    event_targets[target] = 0

        if 'save_event_target_as = ' in text_file:
            event_targets_in_file = re.findall('save_event_target_as = \\w*\\b', text_file)
            if len(event_targets_in_file) > 0:
                for target in event_targets_in_file:
                    target = target[22:].strip()
                    event_targets[target] = 0


# Part 2 - count the number of flag occurrences
    logging.debug(f'{len(event_targets)} defined event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_targets = [i for i in event_targets.keys() if event_targets[i] == 0]

        if 'event_target:' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'event_target:{target}')

        if 'has_event_target =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'has_event_target = {target}')

        if 'global_event_target =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'global_event_target = {target}')

    # Additionally checking yml files for loc functions
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_targets = [i for i in event_targets.keys() if event_targets[i] == 0]

        if '.Get' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'[{target}.GetName')
                event_targets[target] += text_file.count(f'[{target}.GetAdjective')


# Part 3 - throw the error if flag is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    if results != []:
        logging.warning("Following event targets are unused:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} unused targets found.')
        raise AssertionError("Unused targets were encountered! Check console output")