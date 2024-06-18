##########################
# Test script to check if unsupported on_actions are used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ...test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_unsupported_on_actions(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "on_actions_global" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'on_join_faction' in text_file:
            pattern_matches = re.findall("on_join_faction = \\{", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append((match, os.path.basename(filename), "use on_offer_join_faction instead"))

    ResultsReporter.report_results(results=results, message="Unsupported on_actions found. Check console output")
