##########################
# Test script to check if `set_state_category` is used (in KR there are scripted effects that should be used instead)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_set_state_category(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if '00_useful_scripted_effects' in filename:        # Skipped since the effects are stored here
            continue
        text_file = FileOpener.open_text_file(filename)

        if 'set_state_category' in text_file:
            pattern_matches = re.findall('.*set_state_category.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="set_state_category is encountered - use 'increase_state_category_by_one_level = yes' instead. Check console output")
