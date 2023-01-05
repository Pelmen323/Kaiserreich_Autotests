##########################
# Test script to check for flags that are checked before clearing
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import pytest

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


flags_types = [
    "country",
    "global",
    "state"
]


@pytest.mark.parametrize("flag_type", flags_types)
def test_flags_checks(test_runner: object, flag_type: str):
    filepath = test_runner.full_path_to_mod
    results = []
    pattern = "has_" + flag_type + "_flag = (.+\\b).*\\n.*clr_" + flag_type + "_flag = \\1"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if f"clr_{flag_type}_flag" in text_file:

            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append(f"{flag_type} flag - {match}, {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Flags that have excessive checks were encountered. Check console output")
