##########################
# Test script to check for missing character flags
# If flag is not set via "set_character_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
FALSE_POSITIVES = ()


def test_check_missing_character_flags(test_runner: object):
    filepath = test_runner.full_path_to_mod
    character_flags = {}
    paths = {}
# Part 1 - get the dict of entities
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "has_character_flag =" in text_file:
            pattern_matches = re.findall("has_character_flag = [a-zA-Z0-9_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[21:].strip()
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

            pattern_matches = re.findall("has_character_flag = { flag = [a-zA-Z0-9_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[29:].strip()
                    character_flags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - clear false positives and flags with variables:
    # character_flags = DataCleaner.clear_false_positives(input_iter=character_flags, false_positives=FALSE_POSITIVES)

# Part 3 - count the number of entity occurrences
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_flags = [i for i in character_flags.keys() if character_flags[i] == 0]

        if "set_character_flag =" in text_file:
            for flag in not_encountered_flags:
                if flag in text_file:
                    character_flags[flag] += text_file.count(f"set_character_flag = {flag}")
                    character_flags[flag] += text_file.count(f"set_character_flag = {{ flag = {flag}")
                if len(flag) > 3:
                    if flag[-4] == "_":
                        character_flags[flag] += text_file.count(f"set_character_flag = {flag[:-4]}_@root")
                        character_flags[flag] += text_file.count(f"set_character_flag = {flag[:-4]}_@from")
                        character_flags[flag] += text_file.count(f"set_character_flag = {flag[:-4]}_@var:revolter")
                        character_flags[flag] += text_file.count(f"set_character_flag = {{ flag = {flag[:-4]}_@root")
                        character_flags[flag] += text_file.count(f"set_character_flag = {{ flag = {flag[:-4]}_@from")


# Part 4 - throw the error if entity is not used
    results = [i for i in character_flags if character_flags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing character flags were encountered - they are not set via 'set_character_flag'. Check console output")
