##########################
# Test script to check for event targets that are not used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
import logging
FALSE_POSITIVES = ['yunnan_r_kmt_faction_leader', 'nfa_alphonse_juin_target', 'aus_otto_von_habsburg_target',]


def test_check_unused_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'save_global_event_target_as =' in text_file:
            pattern_matches = re.findall('save_global_event_target_as = \\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[29:].strip()
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)

        if 'save_event_target_as = ' in text_file:
            pattern_matches = re.findall('save_event_target_as = \\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[22:].strip()
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - count the number of flag occurrences
    event_targets = DataCleaner.clear_false_positives_dict(input_dict=event_targets, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(event_targets)} defined event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

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
        text_file = FileOpener.open_text_file(filename)

        not_encountered_targets = [i for i in event_targets.keys() if event_targets[i] == 0]

        if '.get' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'[{target}.getname')
                event_targets[target] += text_file.count(f'[{target}.getadjective')


# Part 3 - throw the error if flag is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused event targets were encountered. Check console output")
