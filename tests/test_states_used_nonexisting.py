##########################
# Test script to check for states that are used but they not exist
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_states_used_nonexisting(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_states = f'{test_runner.full_path_to_mod}history\\states\\'
    valid_states = []
    results = []
    paths = {}

    # 1. Extract valid states ids
    for filename in glob.iglob(filepath_to_states + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        states_matches = re.findall("\\tid = (\\d+)", text_file)
        valid_states.append(states_matches[0])

    # 2. Check states in code:
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "common" not in filename and "events" not in filename:   # Skip files that are not important
            continue
        if "names" in filename:                                     # Names files are using the same syntax - don't check them
            continue
        text_file = FileOpener.open_text_file(filename)

        pattern_matches = re.findall("\\t(\\d+) = \\{", text_file)
        pattern_matches += re.findall("target = (\\d+)", text_file)
        pattern_matches += re.findall("state = (\\d+)", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if match not in valid_states and match != "0":      # Don't report `0`
                    results.append(match)
                    paths[match] = os.path.basename(filename)

    ResultsReporter.report_results(results=results, paths=paths, message="Usage of non-existing states encountered. Check console output")
