##########################
# Test script to check for unused state flags
# If flag is not used via "has_state_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import TestClass
import logging
FALSE_POSITIVES = ('ACW_important_state_CSA',     # Wavering momentum flags that are currently unused
                   'ACW_important_state_USA',
                   'ACW_important_state_TEX',
                   'ACW_important_state_PSA',
                   'ACW_important_state_NEE',
                   'was_core_of_ROM',)             # ROM annex event


def test_check_unused_state_flags(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    state_flags = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename).lower()

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
    state_flags = test.clear_false_positives_dict(input_dict=state_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of flag occurrences
    logging.debug(f'{len(state_flags)} set state flags were found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename).lower()

        not_encountered_flags = [i for i in state_flags.keys() if state_flags[i] == 0]

        if 'has_state_flag =' in text_file:
            for flag in not_encountered_flags:
                state_flags[flag] += text_file.count(f'has_state_flag = {flag}')
                state_flags[flag] += text_file.count(f'has_state_flag = {{ flag = {flag}')

# Part 4 - throw the error if flag is not used
    results = [i for i in state_flags if state_flags[i] == 0]
    if results != []:
        logging.warning("Following state flags are not checked via has_state_flag! Recheck them")
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} unused state flags found.')
        raise AssertionError("Unused state flags were encountered! Check console output")
