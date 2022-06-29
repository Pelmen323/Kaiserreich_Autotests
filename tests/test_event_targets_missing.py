##########################
# Test script to check for event targets that are used but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_missing_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    event_targets = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'event_target:' in text_file:
            pattern_matches = re.findall('event_target:\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[13:].strip()
                    event_targets[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(event_targets)} used event targets found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_targets = [i for i in event_targets.keys() if event_targets[i] == 0]

        if 'save_global_event_target_as =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'save_global_event_target_as = {target}')
        if 'save_event_target_as =' in text_file:
            for target in not_encountered_targets:
                event_targets[target] += text_file.count(f'save_event_target_as = {target}')

# Part 3 - throw the error if entity is not used
    results = [i for i in event_targets if event_targets[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Used event targets that are not set were encountered. Check console output")
