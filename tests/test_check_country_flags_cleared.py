##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import TestClass
import logging
FALSE_POSITIVES = ('annexation_window_open', 'liang_refused',)    # Commented functionality


def test_check_cleared_country_flags(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    country_flags = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        if 'clr_country_flag =' in text_file:
            pattern_matches = re.findall('clr_country_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - clear false positives and flags with variables:
    country_flags = test.clear_false_positives_dict(input_dict=country_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of flag occurrences
    logging.debug(f'{len(country_flags)} country flags cleared at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if 'set_country_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f'set_country_flag = {flag}')
                    country_flags[flag] += text_file.count(f'set_country_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    country_flags[flag] += text_file.count(f'set_country_flag = {flag[:-4]}_@root')

# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        logging.warning("Following cleared country flags are not set via set_country_flag! Recheck them")
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} unset country flags found.')
        raise AssertionError("Unset country flags were encountered! Check console output")
