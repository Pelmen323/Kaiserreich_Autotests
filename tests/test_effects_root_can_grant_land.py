##########################
# Test script to check if specific pattern is used that can be replaced with scripted effect (in KR there are scripted effects that should be used instead)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_root_can_grant_land_in_state_scope(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    key_string = "root_can_grant_land"
    pattern = '(^(\\t+)every_owned_state = \\{.*?^\\2\\})'

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if key_string in text_file:

            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if key_string in match[0]:
                        results.append((match[0].replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Root can grant land is used in state scope. This will cause errors in log.")
