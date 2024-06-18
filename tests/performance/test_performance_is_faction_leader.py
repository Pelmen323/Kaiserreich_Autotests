##########################
# Test script to check if `is_faction_leader = yes` is used with `exists = yes` and `is_subject = no`
# (Those are already included in trigger so they are redundant)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_conditions_is_faction_leader(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    all_regex_patterns = []
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+exists = yes.*\\n')
    all_regex_patterns.append('\\t+exists = yes.*\\n\\t+is_faction_leader = yes.*\\n')
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+is_subject = no.*\\n')
    all_regex_patterns.append('\\t+is_subject = no.*\\n\\t+is_faction_leader = yes.*\\n')
    all_regex_patterns.append('\\t+is_faction_leader = yes.*\\n\\t+is_in_faction = yes.*\\n')
    all_regex_patterns.append('\\t+is_in_faction = yes.*\\n\\t+is_faction_leader = yes.*\\n')


# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_faction_leader = yes' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="is_faction_leader = yes necessarily means exists = yes and is_subject = no, so checking for the other two is redundant. Check console output")
