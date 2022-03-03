##########################
# Test script to check for missing cosmetic tags
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import TestClass
import logging


def test_check_cosmetic_tags_missing(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    cosmetic_tags = {}
    paths = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        if 'has_cosmetic_tag =' in text_file:
            pattern_matches = re.findall('has_cosmetic_tag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip().strip('}').strip()
                    cosmetic_tags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - count the number of flag occurrences
    logging.debug(f'{len(cosmetic_tags)} used cosmetic tags were found')
    # Usage directly
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        if 'set_cosmetic_tag =' in text_file:
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += text_file.count(f'set_cosmetic_tag = {flag}')

# Part 3 - throw the error if tag is not used
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    if results != []:
        logging.warning("Following cosmetic tags are unused! Recheck them")
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} unused cosmetic tags found.')
        raise AssertionError("Unused cosmetic tags were encountered! Check console output")
