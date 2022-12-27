##########################
# Test script to check for event targets that are not used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ['previous_overlord', ]


def test_check_unused_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
    paths = {}
    # Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'save_global_event_target_as =' in text_file:
            pattern_matches = re.findall('^[^#]*save_global_event_target_as = (\\w*)\\b', text_file, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)

        if 'save_event_target_as = ' in text_file:
            pattern_matches = re.findall('^[^#]*save_event_target_as = (\\w*)\\b', text_file, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)

    event_targets = DataCleaner.clear_false_positives(input_iter=event_targets, false_positives=FALSE_POSITIVES)
    # Part 2 - count the number of entity occurrences
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

    # Part 3 - throw the error if entity is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused event targets were encountered. Check console output")
