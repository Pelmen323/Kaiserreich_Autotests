##########################
# Test script to check for missing character flags
# If flag is not set via "set_character_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import pytest

from test_classes.generic_test_class import FileOpener, ResultsReporter


@pytest.mark.smoke
def test_check_missing_character_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    character_flags = {}
    paths = {}
    patterns = [r"has_character_flag = \b(\w*)\b", r"has_character_flag = \{.*?flag = \b(\w*)\b"]

    # 1. Get the dict of entities
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "has_character_flag =" in text_file:
            for pattern in patterns:
                pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        character_flags[match] = 0
                        paths[match] = os.path.basename(filename)

    # 2. Count the number of entity occurrences
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]

        if "set_character_flag =" in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += text_file.count(f"set_character_flag = {flag}")
                    character_flags[flag] += text_file.count(f"flag = {flag}")

    # 3. Throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing character flags were encountered - they are not set via 'set_character_flag'")
