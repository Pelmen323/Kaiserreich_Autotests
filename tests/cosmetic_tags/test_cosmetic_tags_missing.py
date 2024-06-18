##########################
# Test script to check for missing cosmetic tags
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ...test_classes.generic_test_class import FileOpener, ResultsReporter, DataCleaner

FALSE_POSITIVES = ["cro_habsburg"]


def test_check_cosmetic_tags_missing(test_runner: object):
    filepath = test_runner.full_path_to_mod
    cosmetic_tags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'has_cosmetic_tag =' in text_file:
            pattern_matches = re.findall('has_cosmetic_tag = ([^ \n\t]+)', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    cosmetic_tags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(cosmetic_tags)} used cosmetic tags were found')
    # Usage directly
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        if 'set_cosmetic_tag =' in text_file:
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += text_file.count(f'set_cosmetic_tag = {flag}')

# Part 3 - throw the error if tag is not used
    cosmetic_tags = DataCleaner.clear_false_positives(input_iter=cosmetic_tags, false_positives=FALSE_POSITIVES)
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing cosmetic tags were encountered. Check console output")
