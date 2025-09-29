##########################
# Test script to check if there is a hidden effect inside a hidden effect
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_effects_hidden_effect(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern = r'^(\t+)hidden_effect = (\{\n.*?)^\1\}'
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "hidden_effect" in text_file:
            pattern_matches = re.findall(pattern, text_file, flags=re.MULTILINE | re.DOTALL)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'hidden_effect' in match[1]:
                        results.append(f"{match[1]} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="there is a hidden effect inside a hidden effect")
