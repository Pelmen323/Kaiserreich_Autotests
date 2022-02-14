##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..imports.file_functions import open_text_file
import logging


def test_check_unused_global_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    global_flags = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = open_text_file(filename)

        if 'set_global_flag =' in text_file:
            pattern_matches = re.findall('set_global_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[18:].strip()
                    global_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('set_global_flag = \\{ flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[27:].strip()
                    global_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - count the number of flag occurrences
    logging.debug(f'{len(global_flags)} set global flags found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = open_text_file(filename)

        not_encountered_flags = [i for i in global_flags.keys() if global_flags[i] == 0]

        if 'has_global_flag =' in text_file:
            for flag in not_encountered_flags:
                global_flags[flag] += text_file.count(f'has_global_flag = {flag}')
                global_flags[flag] += text_file.count(f'has_global_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    global_flags[flag] += text_file.count(f'has_global_flag = {flag[:-4]}_@THIS')

# Part 3 - throw the error if flag is not used
    results = [i for i in global_flags if global_flags[i] == 0]
    if results != []:
        logging.warning("Following global flags are not checked via has_global_flag! Recheck them")
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} unused global flags found.')
        raise AssertionError("Unused global flags were encountered! Check console output")
