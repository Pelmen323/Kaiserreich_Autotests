##########################
# Test script to check if
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import pytest

from test_classes.generic_test_class import FileOpener, ResultsReporter

FALSE_POSITIVES = [
    # AST - not possible to convert
    "unlock_decision_category_tooltip = ast_anderson_policy_decisions"
    # BAT - Already converted
    "unlock_decision_tooltip = bat_zersetzung_decision",
    "unlock_decision_tooltip = bat_banderbekampfung_decision",
    "unlock_decision_tooltip = bat_zerstorungsbataillons_decision",
    "unlock_decision_category_tooltip = bat_eastern_vanguard_decision_category",
]


@pytest.mark.skip(reason="Backlog work")
def test_non_targeted_decisions(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'unlock_decision' in text_file:
            pattern_matches = re.findall('.*unlock_decision.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if match.replace('\t', '') not in FALSE_POSITIVES:
                        results.append((match.replace('\t', ''), os.path.basename(filename)))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=sorted(results), message="Recheck the piece of code and convert to targeted decision if possible. Check console output")
