##########################
# Test script to check for duplicated characters
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
import os
import logging


def test_check_duplicated_characters(test_runner: object):
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    characters = []
    characters_full = []
# Part 1 - get the dict of character usages
    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall('^\t\\w+ =', current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[:-1].strip('\t').strip().lower()
                    characters.append(match[4:])
                    characters_full.append((match[4:], match, os.path.basename(filename)))

# Part 2 - get duplicates
    logging.debug(f'{len(characters)} characters found')  
    results = sorted([(value, characters_full[i]) for i, value in enumerate(characters) if characters.count(value) > 1])

# Part 3 - throw the error if character is not found
    ResultsReporter.report_results(results=results, message="Duplicated characters were encountered. Check console output")
