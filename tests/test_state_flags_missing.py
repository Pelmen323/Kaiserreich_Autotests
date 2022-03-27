##########################
# Test script to check for unassigned state flags
# If flag is not assigned via "set_state_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
import logging


def test_check_missing_state_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    state_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'has_state_flag =' in text_file:
            pattern_matches = re.findall('has_state_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[17:].strip()
                    state_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('has_state_flag = { flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[26:].strip()
                    state_flags[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(state_flags)} state flags used at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in state_flags.keys() if state_flags[i] == 0]

        if 'set_state_flag =' in text_file:
            for flag in not_encountered_flags:
                state_flags[flag] += text_file.count(f'set_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'set_state_flag = {{ flag = {flag}')

# Part 3 - throw the error if entity is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing state flags were encountered. Check console output")
