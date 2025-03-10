##########################
# Test script to check if `set_autonomy` has `end_wars = no` statement
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_effects_set_autonomy(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern = re.compile(r".*[^: \t\n]+\.[^: \t\n]+ = \{")
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        pattern_matches = pattern.findall(text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if 'var:' not in match and 'event_target:' not in match and 'FROM.FROM' not in match:
                    results.append(f"{match} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Add `end_wars = no` to this statement.")
