##########################
# Test script to check for unused country flags
# If flag is not used via "has_country_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file, clear_false_positives_flags
import logging
FALSE_POSITIVES = ('is_han_chinese_tag',        # Currently unused flags
                   'is_non_han_chinese_tag',)


def test_check_unused_country_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    country_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        if 'set_country_flag =' in text_file:
            country_flags_in_file = re.findall('set_country_flag = \\b\\w*\\b', text_file)
            if len(country_flags_in_file) > 0:
                for flag in country_flags_in_file:
                    flag = flag[19:]
                    flag = flag.strip()
                    country_flags[flag] = 0

            country_flags_in_file2 = re.findall('set_country_flag = \\{ flag = \\b\\w*\\b', text_file)
            if len(country_flags_in_file2) > 0:
                for flag in country_flags_in_file2:
                    flag = flag[27:]
                    flag = flag.strip()
                    country_flags[flag] = 0

# Part 2 - clear false positives and flags with variables:
    clear_false_positives_flags(flags_dict=country_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of flag occurrences
    logging.debug(f'{len(country_flags)} set country flags found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_flags = [i for i in country_flags.keys() if country_flags[i] == 0]

        if 'has_country_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    country_flags[flag] += text_file.count(f'has_country_flag = {flag}')
                    country_flags[flag] += text_file.count(f'has_country_flag = {{ flag = {flag}')
                    if country_flags[flag] == 0:    # Performance optimization
                        pattern = 'has_country_flag = \\{\\n\\t*flag = ' + flag
                        country_flags[flag] += len(re.findall(pattern, text_file))

# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        logging.warning("Following country flags are not checked via has_country_flag! Recheck them")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} unused country flags found.')
        raise AssertionError("Unused country flags were encountered! Check console output")
