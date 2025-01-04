##########################
# Test script to check for character flags that are cleared but never set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter

FALSE_POSITIVES = ("was_leader_of_",)


def test_character_flags_cleared(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern_clear = re.compile(r"clr_character_flag = \b(\w*)\b")
    pattern_set = re.compile(r"set_character_flag = \S*")
    character_flags = {}
    paths = {}
    # 1. Get the dict of entities
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "clr_character_flag =" in text_file:
            pattern_matches = pattern_clear.findall(text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

    # 2. Count the number of entity occurrences
    logging.debug(f"{len(character_flags)} character flags cleared at least once")
    assert len(character_flags) > 0, "character_flags must not be empty"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]
        if not_encountered_flags == []:
            break

        if "set_character_flag =" in text_file:
            all_matches = pattern_set.findall(text_file)
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += all_matches.count(f"set_character_flag = {flag}")

    # 3. Throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0 and i not in FALSE_POSITIVES]
    ResultsReporter.report_results(results=results, paths=paths, message="Cleared flags that are never set were encountered. Remove those or set flags")
