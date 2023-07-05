##########################
# Test script to check if `surrender_progress` is used with `has_capitulated` or `has_war`
# (those are redundant - tag will alway be at war if it has surrender progress)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_conditions_surrender_progress(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    list1 = ['has_capitulated = yes', 'has_war =']
    all_regex_patterns = []
    for i in list1:
        all_regex_patterns.append(f'\\t+{i}.*\\n\\t+surrender_progress.*\\n')
        all_regex_patterns.append(f'\\t+surrender_progress.*\\n\\t+{i}.*\\n')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'surrender_progress' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Usage of triggers that include 'has_capitulated', 'has_war', and 'surrender_progress' at the same time is encountered. Check console output")
