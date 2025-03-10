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
    pattern = re.compile(r"(?<!effect_tooltip = \{\n)^(\t*?)set_autonomy = (\{.*?^\1\})", flags=re.DOTALL | re.MULTILINE)
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "history" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        if "set_autonomy" in text_file:
            pattern_matches = pattern.findall(text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "autonomy_state = autonomy_free" not in match[1]:
                        if "end_wars = no" not in match[1] and "end_wars = yes" not in match[1]:
                            m = match[1].replace("\t", "").replace("\n", "  ")
                            results.append(f"{m} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Add `end_wars = no` to this statement.")
