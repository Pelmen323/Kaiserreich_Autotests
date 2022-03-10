##########################
# Test script to check if advisors have missing idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
FALSE_POSITIVES = ('ger_august_von_mackensen', 'qie_wu_peifu',)


def test_check_characters_missing_idea_tokens(test_runner: object):
    filepath = test_runner.full_path_to_mod
    idea_tokens = {}
    paths = {}
# Part 1 - get all used idea tokens
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'activate_advisor' in text_file:
            pattern_matches = re.findall("activate_advisor = [\\w_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip().lower()
                    idea_tokens[match] = 0
                    paths[match] = os.path.basename(filename)
                    
        if 'deactivate_advisor' in text_file:
            pattern_matches = re.findall("deactivate_advisor = [\\w_']*", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[21:].strip().lower()
                    idea_tokens[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - find what idea tokens are used
    idea_tokens = DataCleaner.clear_false_positives_dict(input_dict=idea_tokens, false_positives=FALSE_POSITIVES)
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
         
        not_encountered_tokens = [i for i in idea_tokens.keys() if idea_tokens[i] == 0]         
        if 'idea_token' in text_file:
            for token in not_encountered_tokens:
                pattern = f'idea_token = {token}\\b'
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    idea_tokens[token] += 1

# Part 2 - throw the error any idea token is missing
    results = [i for i in idea_tokens.keys() if idea_tokens[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Advisors activation with missing idea tokens were encountered. Check console output")
