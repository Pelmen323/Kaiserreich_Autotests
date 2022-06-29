##########################
# Test script to check if `exists = yes` trigger is used with triggers that already include that trigger
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_conditions_exists_yes(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - prepare the list of patterns
    list1 = ['is_in_faction = yes', 'is_in_faction_with', 'has_war_with', 'has_war = yes', 'owns_state', 'is_subject = yes', 'is_subject_of', 'is_in_tech_sharing_group', 'is_ally_of_root = yes']
    all_regex_patterns = []
    for i in list1:
        all_regex_patterns.append(f'\\t+{i}.*\\n\\t+exists = yes.*\\n')
        all_regex_patterns.append(f'\\t+exists = yes.*\\n\\t+{i}.*\\n')

# Part 2 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'exists = yes' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 3 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Usage of triggers that include 'exists = yes', and 'exists = yes' at the same time is encountered. Check console output")
