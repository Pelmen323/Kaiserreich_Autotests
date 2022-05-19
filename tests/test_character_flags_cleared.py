##########################
# Test script to check for character flags that are cleared but never set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
import logging


def test_check_cleared_character_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    character_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'clr_character_flag =' in text_file:
            pattern_matches = re.findall('clr_character_flag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[21:].strip()
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(character_flags)} character flags cleared at least once')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]

        if 'set_character_flag =' in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += text_file.count(f'set_character_flag = {flag}')
                    character_flags[flag] += text_file.count(f'set_character_flag = {{ flag = {flag}')
                if flag[-4] == '_':
                    character_flags[flag] += text_file.count(f'set_character_flag = {flag[:-4]}_@root')

# Part 3 - throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Cleared flags that are never set were encountered. Check console output")
