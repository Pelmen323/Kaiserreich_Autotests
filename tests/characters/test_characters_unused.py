##########################
# Test script to check for characters that exist but never recruited
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import re

from ...test_classes.characters_class import Characters
from ...test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_unused_characters(test_runner: object):
    path_to_history_files = f'{test_runner.full_path_to_mod}history\\'
    characters = {}
# Part 1 - get all existing characters names
    characters_names, paths = Characters.get_all_characters_names(test_runner=test_runner, return_paths=True)
    for i in characters_names:
        characters[i] = 0

# Part 2 - get list of char recruitments
    logging.debug(f'{len(characters)} characters found')
    for filename in glob.iglob(path_to_history_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_chars = [i for i in characters.keys() if characters[i] == 0]

        if 'recruit_character =' in text_file:
            for char in not_encountered_chars:
                pattern = f'recruit_character = {char}\\b'
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    characters[char] += 1

# Part 3 - throw the error if character is not found
    results = [i for i in characters.keys() if characters[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused (not recruited) characters were encountered. Check console output")
