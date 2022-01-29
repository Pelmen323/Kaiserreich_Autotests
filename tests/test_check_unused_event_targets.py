##########################
# Test script to check for event targets that are not used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file


def test_check_unused_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
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
    print(f'{len(event_targets)} defined event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if 'event_target:' in text_file:
            for target in event_targets.keys():
                event_targets[target] += text_file.count(f'event_target:{target}')

        if 'has_event_target =' in text_file:
            for target in [i for i in event_targets.keys() if event_targets[i] == 0]:
                event_targets[target] += text_file.count(f'has_event_target = {target}')

        if 'global_event_target =' in text_file:
            for target in [i for i in event_targets.keys() if event_targets[i] == 0]:
                event_targets[target] += text_file.count(f'global_event_target = {target}')

    # Additionally checking yml files for loc functions
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        if '.Get' in text_file:
            for target in [i for i in event_targets.keys() if event_targets[i] == 0]:
                event_targets[target] += text_file.count(f'[{target}.GetName')
                event_targets[target] += text_file.count(f'[{target}.GetAdjective')


# Part 3 - throw the error if flag is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    if results != []:
        print("Following event targets are unused:")
        for i in results:
            print(f'- [ ] {i}')
        print(f'{len(results)} unused targets found.')
        raise AssertionError("Unused targets were encountered! Check console output")
