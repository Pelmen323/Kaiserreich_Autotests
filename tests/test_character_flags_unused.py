##########################
# Test script to check for unused character flags
# If flag is not used via "has_character_flag" at least once, it will appear in test results
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

FALSE_POSITIVES = ('is_han_chinese_tag',        # Currently unused flags
                   'is_non_han_chinese_tag',)


def test_check_unused_character_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    character_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'set_character_flag =' in text_file:
            pattern_matches = re.findall("set_character_flag = \\b[\\w']*\\b", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[21:].strip()
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches2 = re.findall("set_character_flag = \\{ flag = \\b[\\w']*\\b", text_file)
            if len(pattern_matches2) > 0:
                for match in pattern_matches2:
                    match = match[29:].strip()
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - clear false positives and flags with variables:
    character_flags = DataCleaner.clear_false_positives(input_iter=character_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    logging.debug(f'{len(character_flags)} set character flags found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]

        if 'has_character_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += text_file.count(f'has_character_flag = {flag}')
                    character_flags[flag] += text_file.count(f'has_character_flag = {{ flag = {flag}')
                    if character_flags[flag] == 0:    # Performance optimization
                        pattern = 'has_character_flag = \\{\\n\\t*flag = ' + flag
                        character_flags[flag] += len(re.findall(pattern, text_file))

# Part 4 - throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused character flags were encountered - they are not used via 'has_character_flag' at least once. Check console output")
