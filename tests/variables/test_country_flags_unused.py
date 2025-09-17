##########################
# Test script to check for unused country flags
# If flag is not used via "has_country_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = (
    'is_han_chinese_tag',
    'is_non_han_chinese_tag',
    'saf_antagonise_maf',
    'saf_antagonise_nmb',
    'ins_high_unity',
    'can_integrate_lec',
    'can_integrate_tai',
    'can_integrate_xxa',
    'can_integrate_50_xxa',
    'can_integrate_80_xxa',
    'can_integrate_80_',
)


def test_check_unused_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
    paths = {}
# 1. get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'set_country_flag =' in text_file:
            pattern_matches = re.findall("set_country_flag = \\b[\\w']*\\b", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches2 = re.findall("set_country_flag = \\{ flag = \\b[\\w']*\\b", text_file)
            if len(pattern_matches2) > 0:
                for match in pattern_matches2:
                    match = match[27:].strip()
                    country_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# 2. clear false positives and flags with variables:
    country_flags = DataCleaner.clear_false_positives(input_iter=country_flags, false_positives=FALSE_POSITIVES)

# 3. count the number of entity occurrences
    logging.debug(f'{len(country_flags)} set country flags found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if 'has_country_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f'has_country_flag = {flag}')
                    country_flags[flag] += text_file.count(f'has_country_flag = {{ flag = {flag}')
                    if country_flags[flag] == 0:    # Performance optimization
                        pattern = 'has_country_flag = \\{\\n\\t*flag = ' + flag
                        country_flags[flag] += len(re.findall(pattern, text_file))

# 4. throw the error if entity is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused country flags were encountered - they are not used via 'has_country_flag' at least once.")
