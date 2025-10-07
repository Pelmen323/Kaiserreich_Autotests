##########################
# Test script to check for missing flags
# If flag is not set via "set_xxx_flag" at least once, it will appear in test results
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import pytest
from test_classes.variables_class import Variables
from test_classes.generic_test_class import (
    ResultsReporter,
    DataCleaner,
)

FALSE_POSITIVES_GENERIC = [
    "@",
]

FALSE_POSITIVES_COUNTRY = [
    "@",
    "ire_got_guarantee",
    "ire_rejected_guarantee",
    "nfa_rebelled",
    "ire_alliance_refused",
    "nfa_previously_rebelled",
    "rom_deal",
    "rus_can_core",
    "sent_volunteers",
    "china_refused_alliance",
]

input_list = [
    ["country", FALSE_POSITIVES_COUNTRY],
    ["global", FALSE_POSITIVES_GENERIC],
    ["state", FALSE_POSITIVES_GENERIC],
]


@pytest.mark.parametrize("input_list", input_list)
def test_missing_flags(test_runner: object, input_list):
    flag_type = input_list[0]
    false_positives = input_list[1]
    results = []
    used_flags, paths = Variables.get_all_used_flags(test_runner=test_runner, lowercase=True, flag_type=flag_type, return_paths=True)
    set_flags = Variables.get_all_set_flags(test_runner=test_runner, lowercase=True, flag_type=flag_type)
    used_flags = DataCleaner.clear_false_positives_partial_match(used_flags, false_positives)

    for i in used_flags:
        if i not in set_flags:
            results.append(f"{i:<55}{os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message=f"Missing {flag_type} flags were encountered - they are not set via 'set_{flag_type}_flag'. Flags with @ are skipped.")
