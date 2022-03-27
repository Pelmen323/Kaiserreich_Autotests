##########################
# Test script to check for non-assigned global flags
# If flag is not used via "set_global_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
import logging
FALSE_POSITIVES = ('kr_economy_logging',)


def test_check_missing_global_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    global_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'has_global_flag =' in text_file:
            pattern_matches = re.findall('has_global_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[18:].strip()
                    global_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('has_global_flag = { flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[27:].strip()
                    global_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - clear false positives and flags with variables:
    global_flags = DataCleaner.clear_false_positives(input_iter=global_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    logging.debug(f'{len(global_flags)} global flags used at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in global_flags.keys() if global_flags[i] == 0]

        if 'set_global_flag =' in text_file:
            for flag in not_encountered_flags:
                global_flags[flag] += text_file.count(f'set_global_flag = {flag}')
                global_flags[flag] += text_file.count(f'set_global_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    global_flags[flag] += text_file.count(f'set_global_flag = {flag[:-4]}_@root')
                    global_flags[flag] += text_file.count(f'set_global_flag = {flag[:-4]}_@from')

# Part 4 - throw the error if entity is not used
    results = [i for i in global_flags if global_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Global flags that are used but not set were encountered. Check console output")
