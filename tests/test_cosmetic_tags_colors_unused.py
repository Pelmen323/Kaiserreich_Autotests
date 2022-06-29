##########################
# Test script to check for unused cosmetic tags - colors
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ["cro_habsburg"]


def test_check_cosmetic_tags_colors_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_cosmetic = f'{test_runner.full_path_to_mod}common\\countries\\cosmetic.txt'
    cosmetic_tags = {}
# Part 1 - get the dict of all cosmetic tags
    text_file = FileOpener.open_text_file(filepath_cosmetic)

    text_file_splitted = text_file.split('\n')[1:]
    for line in range(len(text_file_splitted)):
        current_line = text_file_splitted[line]
        pattern_matches = re.findall('^\\w+', current_line)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                cosmetic_tags[match] = 0

# Part 2 - count the number of tag occurrences
    logging.debug(f'{len(cosmetic_tags)} cosmetic tags colors were found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        if 'set_cosmetic_tag =' in text_file:
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += text_file.count(f'set_cosmetic_tag = {flag}')

# Part 4 - throw the error if tag is not used
    cosmetic_tags = DataCleaner.clear_false_positives(input_iter=cosmetic_tags, false_positives=FALSE_POSITIVES)
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    ResultsReporter.report_results(results=results, message="common\\countries\\cosmetic.txt - unused cosmetic tags colors were encountered. Check console output")
