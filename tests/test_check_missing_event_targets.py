##########################
# Test script to check for event targets that are used but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file


def test_check_missing_event_targets(test_runner: object):
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

        if 'event_target:' in text_file:
            event_targets_in_file = re.findall('event_target:\\w*\\b', text_file)
            if len(event_targets_in_file) > 0:
                for target in event_targets_in_file:
                    target = target[13:].strip()
                    event_targets[target] = 0


# Part 2 - count the number of flag occurrences
    print(f'{len(event_targets)} used event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
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
        print("Following event targets are used but never set:")
        for i in results:
            print(f'- [ ] {i}')
        raise AssertionError("Missing event targets were encountered! Check console output")
