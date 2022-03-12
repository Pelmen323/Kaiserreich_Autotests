##########################
# Test script to check for characters that exist but never recruited
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
import logging


def test_check_unused_characters(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    characters = {}
# Part 1 - get all existing characters
    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall('^\t\\w+ =', current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[:-1].strip('\t').strip().lower()
                    characters[match] = 0

# Part 2 - get list of char recruitments
    logging.debug(f'{len(characters)} characters found')
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_chars = [i for i in characters.keys() if characters[i] == 0]

        if 'recruit_character =' in text_file:
            for char in  not_encountered_chars:
                pattern = f'recruit_character = {char}\\b'
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    characters[char] += 1

# Part 3 - throw the error if character is not found
    results = [i for i in characters.keys() if characters[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused (not recruited) characters were encountered. Check console output")
