##########################
# Test script to check if if they_accept/refuse tts are not followed with effect_tooltip
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import pytest
import re
from test_classes.generic_test_class import ResultsReporter, FileOpener


tooltip_list = [
    "if_they_accept_tt",
    "if_they_refuse_tt",
]


@pytest.mark.parametrize("tooltip", tooltip_list)
def test_flags_checks(test_runner: object, tooltip: str):
    filepath = test_runner.full_path_to_mod
    pattern = r"custom_effect_tooltip = " + tooltip + r".*\n(.*\n.*)"
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        # if "FRA effects" in filename:
        #     continue
        text_file = FileOpener.open_text_file(filename)

        if tooltip in text_file:
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "effect_tooltip" not in match and "event_option_tooltip" not in match:
                        results.append(f"{match} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Issues with effect_tooltip were encountered - if if they_accept/refuse tts are not followed with effect_tooltip")
