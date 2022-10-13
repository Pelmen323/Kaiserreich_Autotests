##########################
# Test script to check for strategies without allowed check
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = [
    "war_propaganda",
]


def test_decisions_without_allowed_check(test_runner: object):
    filepath_to_strategies = f'{test_runner.full_path_to_mod}common\\ai_strategy\\'
    results = []

    # 1. Extract the ai strategies without allowed check

    for filename in glob.iglob(filepath_to_strategies + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        strategies_matches = re.findall("^\\w* = \\{.*?^\\}", text_file, flags=re.DOTALL | re.MULTILINE)
        if len(strategies_matches) > 0:
            for strategy_match in strategies_matches:
                strategy_name = re.findall("^(.*) = \\{", strategy_match)
                if "allowed = {" not in strategy_match:
                    if "always = yes" not in strategy_match:
                        results.append(strategy_name[0])

# Part 3 - throw the error if entity is not used
    results = DataCleaner.clear_false_positives(input_iter=results, false_positives=FALSE_POSITIVES)
    ResultsReporter.report_results(results=results, message="Strategies without allowed trigger were encountered. Check console output")
