##########################
# Test script to check if
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


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
                    results.append((match.replace('\t', ''), os.path.basename(filename)))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Recheck the piece of code and convert to targeted decision if possible. Check console output")
