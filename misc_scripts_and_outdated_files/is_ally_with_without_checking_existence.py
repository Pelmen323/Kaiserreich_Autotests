##########################
# Test script to check if is_ally_with is used without checking tag's existence
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
import os
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


@pytest.mark.skip(reason="Disabled for now")
def test_check_is_ally_with(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

# Part 1 - perform search
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_ally_with' in text_file:
            pattern_matches = re.findall('.*\\n.*is_ally_with.*\\n.*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'country_exists =' not in match and 'exists = yes' not in match:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

# Part 1 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="is_ally_with w/o 'country_exists =' or 'exists = yes' is encountered. Check console output")
