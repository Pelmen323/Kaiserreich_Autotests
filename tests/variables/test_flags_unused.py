##########################
# Test script to check for unused flags
# If flag is not used via "has_xxx_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import pytest
from test_classes.variables_class import Variables
from test_classes.generic_test_class import (
    DataCleaner,
    ResultsReporter,
)

FALSE_POSITIVES_GENERIC = [
    "@",
    "[",
]

FALSE_POSITIVES_COUNTRY = [
    "@",
    "[",
    "saf_antagonise_",
    "default_puppet",
]

FALSE_POSITIVES_GLOBAL = [
    "@",
    "[",
    "kr_current_version",
]

input_list = [
    ["country", FALSE_POSITIVES_COUNTRY],
    ["global", FALSE_POSITIVES_GLOBAL],
    ["state", FALSE_POSITIVES_GENERIC],
]


@pytest.mark.parametrize("input_list", input_list)
def test_unused_flags(test_runner: object, input_list):
    flag_type = input_list[0]
    false_positives = input_list[1]
    results = []
    set_flags, paths = Variables.get_all_set_flags(test_runner=test_runner, lowercase=True, flag_type=flag_type, return_paths=True)
    used_flags = Variables.get_all_used_flags(test_runner=test_runner, lowercase=True, flag_type=flag_type)
    set_flags = DataCleaner.clear_false_positives_partial_match(set_flags, false_positives)

    for i in set_flags:
        if i not in used_flags:
            results.append(f"{i:<55} {os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message=f"Unused {flag_type} flags were encountered - they are not used via 'has_{flag_type}_flag' at least once. Flags with @ are skipped.")
