##########################
# Test script to check for characters that exist but are never recruited
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.characters_class import Characters
from test_classes.generic_test_class import FileOpener, ResultsReporter
from pathlib import Path


def test_check_unused_characters(test_runner: object):
    path_to_history_files = Path(test_runner.full_path_to_mod) / "history"
    path_pattern = str(path_to_history_files / "**/*.txt")
    pattern = re.compile(r"recruit_character = \S*")
    found_files = False
    characters = {}
    # 1. Get all existing characters names
    characters_names, paths = Characters.get_all_characters_names(test_runner=test_runner, return_paths=True)
    for i in characters_names:
        characters[i] = 0

    # 2. Get list of char recruitments
    for filename in glob.iglob(path_pattern, recursive=True):
        found_files = True
        text_file = FileOpener.open_text_file(filename)

        not_encountered_chars = [i for i in characters.keys() if characters[i] == 0]
        if not_encountered_chars == []:
            break

        if "recruit_character =" in text_file:
            # Reduces execution time by 98% compared to searching just in text_file
            all_recruit_character_matches = re.findall(pattern, text_file)
            for char in not_encountered_chars:
                if f"recruit_character = {char}" in all_recruit_character_matches:
                    characters[char] += 1

    assert found_files, f"No .txt files found matching pattern: {path_pattern}"
    results = [i for i in characters.keys() if characters[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused (not recruited) characters were encountered.")
