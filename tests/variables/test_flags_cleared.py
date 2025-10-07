##########################
# Test script to check for flags that are cleared but never set
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import pytest
from test_classes.variables_class import Variables
from test_classes.generic_test_class import ResultsReporter, DataCleaner

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
def test_cleared_flags(test_runner: object, input_list):
    flag_type = input_list[0]
    false_positives = input_list[1]
    results = []
    cleared_flags, paths = Variables.get_all_cleared_flags(test_runner=test_runner, lowercase=True, flag_type=flag_type, return_paths=True)
    set_flags = Variables.get_all_set_flags(test_runner=test_runner, flag_type=flag_type, lowercase=True)
    cleared_flags = DataCleaner.clear_false_positives_partial_match(cleared_flags, false_positives)

    for i in cleared_flags:
        if i not in set_flags:
            results.append(f"{i:<55}{os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message=f"Cleared {flag_type} flags that are never set were encountered. Flags with @ are skipped.")
