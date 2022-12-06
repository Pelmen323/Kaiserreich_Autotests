##########################
# Test script to check for unused state flags
# If flag is not used via "has_state_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
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

FALSE_POSITIVES = ('acw_important_state_csa',     # Wavering momentum flags that are currently unused
                   'acw_important_state_usa',
                   'acw_important_state_tex',
                   'acw_important_state_psa',
                   'acw_important_state_nee',
                   'was_core_of_rom',             # ROM annex event
                   'temporary_occupied_by_',
                   )


def test_check_unused_state_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    state_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'set_state_flag =' in text_file:
            pattern_matches = re.findall('set_state_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[17:].strip()
                    state_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('set_state_flag = \\{ flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[26:].strip()
                    state_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - clear false positives and flags with variables:
    state_flags = DataCleaner.clear_false_positives(input_iter=state_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    logging.debug(f'{len(state_flags)} set state flags were found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in state_flags.keys() if state_flags[i] == 0]

        if 'has_state_flag =' in text_file:
            for flag in not_encountered_flags:
                state_flags[flag] += text_file.count(f'has_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'has_state_flag = {{ flag = {flag}')

# Part 4 - throw the error if entity is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused state flags were encountered - they are not used via 'has_state_flag' at least once. Check console output")
