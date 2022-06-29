##########################
# Test script to check for missing characters that are checked via 'has_character' or 'character ='
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ..test_classes.characters_class import Characters
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_missing_characters(test_runner: object):
    filepath = test_runner.full_path_to_mod
    characters_usages = []
    characters_names = []
    paths = {}
    # Get all character usages
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "on_actions_global" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'has_character =' in text_file:
            pattern_matches = re.findall('has_character = \\w*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[15:].strip().lower()
                    characters_usages.append(match)
                    paths[match] = os.path.basename(filename)

        if 'character =' in text_file:
            pattern_matches = re.findall('\\bcharacter = \\w*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'event_target' not in match:
                        match = match[11:].strip().lower()
                        characters_usages.append(match)
                        paths[match] = os.path.basename(filename)

            pattern_matches = re.findall('\\bis_character = \\w*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'event_target' not in match:
                        match = match[14:].strip().lower()
                        characters_usages.append(match)
                        paths[match] = os.path.basename(filename)

    logging.debug(f'{len(characters_usages)} character usages found')

    # Get all characters names
    characters_names = Characters.get_all_characters_names(test_runner=test_runner, return_paths=False)

    results = [i for i in characters_usages if i not in characters_names]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing characters were encountered. Check console output")
