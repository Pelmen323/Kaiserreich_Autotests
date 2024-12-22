##########################
# Test script to check for unused character flags
# If flag is not used via "has_character_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ("was_leader_of_",)


def test_character_flags_unused(test_runner: object):
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
    logging.debug(f"{len(character_flags)} character flags encountered")
    assert len(character_flags) > 0, "character_flags must not be empty"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]
        if not_encountered_flags == []:
            break

        if "has_character_flag =" in text_file:
            all_matches = re.findall(r"has_character_flag = [^ \n\t]*", text_file)
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += all_matches.count(f"has_character_flag = {flag}")
                    if "has_character_flag = { flag = " + flag in text_file:
                        character_flags[flag] += 1

    # 3. Throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0 and i not in FALSE_POSITIVES]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused character flags were encountered - they are not used via 'has_character_flag'")
