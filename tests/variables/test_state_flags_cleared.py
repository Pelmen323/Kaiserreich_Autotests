##########################
# Test script to check for state flags that are cleared but not set
# If flag is not set via "set_state_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_cleared_state_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    state_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'clr_state_flag =' in text_file:
            pattern_matches = re.findall('clr_state_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[17:].strip()
                    state_flags[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(state_flags)} state flags cleared at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in state_flags.keys() if state_flags[i] == 0]

        if 'set_state_flag =' in text_file:
            for flag in not_encountered_flags:
                state_flags[flag] += text_file.count(f'set_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'set_state_flag = {{ flag = {flag}')

# Part 3 - throw the error if entity is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="State flags that are cleared but not set were encountered. Check console output")
