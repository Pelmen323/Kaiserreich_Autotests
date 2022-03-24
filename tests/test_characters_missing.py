##########################
# Test script to check for missing characters that are checked via 'has_character' or 'character ='
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
import logging


def test_check_missing_characters(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    characters_usages = {}
    characters = []
    paths = {}
# Part 1 - get the dict of character usages
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "on_actions_global" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'has_character =' in text_file:
            pattern_matches = re.findall('has_character = \\w*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[15:].strip().lower()
                    characters_usages[match] = 0
                    paths[match] = os.path.basename(filename)

        if 'character =' in text_file:
            pattern_matches = re.findall('\\bcharacter = \\w*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'event_target' not in match:
                        match = match[11:].strip().lower()
                        characters_usages[match] = 0
                        paths[match] = os.path.basename(filename)


# Part 2 - get list of all characters
    logging.debug(f'{len(characters_usages)} unique character usages found')

# Part 3 - get the dict of character usages
    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall('^\t\\w+ =', current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[:-1].strip('\t').strip().lower()
                    characters.append(match)

# Part 4 - find if character is present
    for item in characters_usages:
        for character in characters:
            if character in item:
                characters_usages[item] += 1

# Part 5 - throw the error if character is not found
    results = [i for i in characters_usages.keys() if characters_usages[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing characters were encountered. Check console output")
