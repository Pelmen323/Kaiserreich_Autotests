##########################
# Test script to check is unoptimised combination of conditions is used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from itertools import permutations


def test_check_conditions_is_ally_with(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    paths = {}

# Part 1 - prepare the list of patterns
    possible_parts_of_pattern = ['\\t+tag =.*\\n', '\\t+is_in_faction_with.*\\n', '\\t+is_subject_of.*\\n']
    all_regex_patterns_raw = list(permutations(possible_parts_of_pattern))
    all_regex_patterns = []
    for pattern in all_regex_patterns_raw:
        all_regex_patterns.append(''.join(pattern))
    all_regex_patterns.append('.*\\{.*\\n\\t+is_in_faction_with.*\\n\\t+is_subject_of.*\\n.*\\}')
    all_regex_patterns.append('.*\\{.*\\n\\t+is_subject_of.*\\n\\t+is_in_faction_with.*\\n.*\\}')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_subject_of' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append(match)
                        paths[match] = os.path.basename(filename)

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, paths=paths, message="'is_ally_with' condition can be used in the mentioned files instead. Check console output")


def test_check_conditions_is_faction_leader(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    all_regex_patterns = []
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+exists = yes.*\\n')
    all_regex_patterns.append('\\t+exists = yes.*\\n\\t+is_faction_leader = yes.*\\n')
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+is_subject = no.*\\n')
    all_regex_patterns.append('\\t+is_subject = no.*\\n\\t+is_faction_leader = yes.*\\n')


# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_faction_leader = yes' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match, os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="is_faction_leader = yes necessarily means exists = yes and is_subject = no, so checking for the other two is redundant. Check console output")
