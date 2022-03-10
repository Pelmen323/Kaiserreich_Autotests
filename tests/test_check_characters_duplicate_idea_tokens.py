##########################
# Test script to check if advisors have duplicated idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


def test_check_characters_advisors_duplicate_idea_tokens(test_runner: object):
    filepath = test_runner.full_path_to_mod
    idea_tokens = []
# Part 1 - get all idea tokens
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'idea_token' in text_file:
            pattern_matches = re.findall("idea_token = [\\w_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '_sic' not in match:                 # Second in command ideas can be assigned in multiple places
                        match = match[13:].strip().lower()
                        idea_tokens.append(match)

# Part 2 - throw the error any idea token is used twice
    results = sorted(list(set([i for i in idea_tokens if idea_tokens.count(i) > 1])))
    ResultsReporter.report_results(results=results, message="Advisors with non-unique idea tokens were encountered. Check console output")
