##########################
# Test script to check for states that are used but they not exist
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_decisions_without_allowed_check(test_runner: object):
    filepath_to_states = f'{test_runner.full_path_to_mod}history\\states\\'
    filepath_common = f'{test_runner.full_path_to_mod}common\\'
    filepath_events = f'{test_runner.full_path_to_mod}events\\'
    valid_states = []
    results = []
    paths = {}

    # 1. Extract valid states ids
    for filename in glob.iglob(filepath_to_states + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        states_matches = re.findall("\\tid = (\\d+)", text_file)
        valid_states.append(states_matches[0])

    # 2. Check states in code:
    # Common
    for filename in glob.iglob(filepath_common + '**/*.txt', recursive=True):
        if "names" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        pattern_matches = re.findall("\\t(\\d+) = \\{", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if match not in valid_states:
                    results.append(match)
                    paths[match] = os.path.basename(filename)

    # Events
    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        pattern_matches = re.findall("\\t(\\d+) = \\{", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if match not in valid_states:
                    results.append(match)
                    paths[match] = os.path.basename(filename)

        pattern_matches = re.findall("target = (\\d+)", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if match not in valid_states:
                    results.append(match)
                    paths[match] = os.path.basename(filename)

    ResultsReporter.report_results(results=results, paths=paths, message="Usage of non-existing states encountered. Check console output")
