##########################
# Test script to check if every xxx state is used with `is_owned_by = root` (this check is redundant)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


list_of_triggers = [
    "every_owned_state",
    "all_owned_state",
    "any_owned_state",
    "random_owned_state",
]


@pytest.mark.parametrize("trigger", list_of_triggers)
def test_check_syntax_xxx_owned_state(test_runner: object, trigger):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if trigger in text_file:
            pattern = f'^(\\t*?){trigger}'+' = (\\{\n.*?^\\1\\})'
            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "\tis_owned_by = root" in match[1]:
                        results.append((match[1], os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Is owned by root is redundant here. Check console output")
