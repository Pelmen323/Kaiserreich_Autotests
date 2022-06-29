##########################
# Test script to check for country flags that are cleared but never set
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

FALSE_POSITIVES = ('annexation_window_open', 'liang_refused',)    # Commented functionality


def test_check_cleared_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'clr_country_flag =' in text_file:
            pattern_matches = re.findall('clr_country_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)


# Part 2 - clear false positives and flags with variables:
    country_flags = DataCleaner.clear_false_positives(input_iter=country_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    logging.debug(f'{len(country_flags)} country flags cleared at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if 'set_country_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f'set_country_flag = {flag}')
                    country_flags[flag] += text_file.count(f'set_country_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    country_flags[flag] += text_file.count(f'set_country_flag = {flag[:-4]}_@root')

# Part 4 - throw the error if entity is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Cleared flags that are never set were encountered. Check console output")
